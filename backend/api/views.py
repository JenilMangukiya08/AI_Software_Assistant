from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatSerializer
from .serializers import RepositorySerializer
from rag.qa import ask_repository
from github.clone import clone_repository
from rag.pipeline import index_repository
from graph.workflow import graph
from utils.file_tree import build_tree
from utils.repository_stats import get_repository_stats
from utils.symbol_search import search_symbol
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Repository,ChatSession,ChatMessage
from .serializers import ChatSessionSerializer
from rag.chroma_store import ChromaVectorStore
from rag.memory import get_memory


import shutil
import os


class RepositoryUploadView(APIView):
    permission_classes=[

            IsAuthenticated

        ]

    def post(self, request):
        
        serializer = RepositorySerializer(data=request.data)
       

        if serializer.is_valid():

            url = serializer.validated_data["url"]
            repo_path = clone_repository(url)
            print("Repository URL:", url)
            print("Cloned Path:", repo_path)
            index_repository(repo_path)
            repo_name = os.path.basename(repo_path)

            Repository.objects.get_or_create(

                user=request.user,
                github_url=url,

                defaults={
                    "name": repo_name,
                    "collection_name": repo_name
                }

            )       

            return Response({
                "message": "Repository indexed successfully.",
                "repository":repo_name
            })

        return Response(serializer.errors, status=400)


class ChatAPIView(APIView):
    permission_classes=[
        IsAuthenticated
    ]

    def post(self, request):

        print("Request Data:", request.data)

        serializer = ChatSerializer(data=request.data)

        if not serializer.is_valid():
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=400)

        repository_name = serializer.validated_data["repository"]
        question = serializer.validated_data["question"]
        repository = Repository.objects.get(
            user=request.user,
            collection_name=repository_name
        )
        session_id = serializer.validated_data.get("session_id")

        if session_id:

            session = ChatSession.objects.get(
                id=session_id,
                user=request.user
            )

        else:

            session = ChatSession.objects.create(
                user=request.user,
                repository=repository,
                title=question[:50]
            )

        ChatMessage.objects.create(
            session=session,
            sender="user",
            message=question
        )
        memory = get_memory(session)
        

        result = ask_repository(repository_name, question,memory)

        ChatMessage.objects.create(
            session=session,
            sender="ai",
            message=result["answer"]
        )

        return Response({
            "answer": result["answer"],
            "sources": result["sources"],
            "session_id": session.id
        })
    
class RepositoryTreeView(APIView):

    def get(self, request):

        repository = request.GET.get("repository")

        path = os.path.join(
            "repositories",
            repository
        )

        tree = build_tree(path)

        return Response(tree)
    


class RepositoryStatsView(APIView):

    def get(self, request):

        repository = request.GET.get("repository")

        repo_path = os.path.join(
            "repositories",
            repository
        )

        stats = get_repository_stats(repo_path)

        return Response(stats)
    

class SymbolSearchView(APIView):

    def get(self,request):

        repository=request.GET.get("repository")

        symbol=request.GET.get("symbol")

        repo_path=os.path.join(
            "repositories",
            repository
        )

        results=search_symbol(
            repo_path,
            symbol
        )

        return Response(results)
    
class RegisterView(APIView):

    authentication_classes=[]

    permission_classes=[]

    def post(self,request):

        serializer=RegisterSerializer(

            data=request.data

        )

        if serializer.is_valid():

            serializer.save()

            return Response({

                "message":"User Registered Successfully"

            })

        return Response(

            serializer.errors,

            status=400

        )
    


class ChatHistoryAPIView(APIView):

    permission_classes = [

        IsAuthenticated

    ]

    def get(self, request):

        sessions = ChatSession.objects.filter(

            user=request.user

        ).order_by("-created_at")

        serializer = ChatSessionSerializer(

            sessions,

            many=True

        )

        return Response(serializer.data)
    

class ChatMessagesAPIView(APIView):

    permission_classes = [

        IsAuthenticated

    ]

    def get(self, request, session_id):

        session = ChatSession.objects.get(

            id=session_id,

            user=request.user

        )

        messages = ChatMessage.objects.filter(

            session=session

        ).order_by("created_at")

        data = []

        for message in messages:

            data.append({

                "sender": message.sender,

                "text": message.message

            })

        return Response(data)
    
class DeleteChatAPIView(APIView):

    permission_classes = [

        IsAuthenticated

    ]

    def delete(self, request, session_id):

        session = ChatSession.objects.get(

            id=session_id,

            user=request.user

        )

        session.delete()

        return Response({

            "message":"Deleted"

        })
    

class RenameChatAPIView(APIView):

    permission_classes = [

        IsAuthenticated

    ]

    def put(self, request, session_id):

        session = ChatSession.objects.get(

            id=session_id,

            user=request.user

        )

        session.title = request.data["title"]

        session.save()

        return Response({

            "message":"Updated"

        })
    

class ProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        repository_count = Repository.objects.filter(
            user=user
        ).count()

        session_count = ChatSession.objects.filter(
            user=user
        ).count()

        message_count = ChatMessage.objects.filter(
            session__user=user
        ).count()

        return Response({

            "username": user.username,

            "email": user.email,

            "date_joined": user.date_joined,

            "repositories": repository_count,

            "chat_sessions": session_count,

            "messages": message_count

        })
    

class RepositoryListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        repositories = Repository.objects.filter(
            user=request.user
        ).order_by("-uploaded_at")

        data = []

        for repo in repositories:

            data.append({

                "id": repo.id,

                "name": repo.name,

                "github_url": repo.github_url,

                "uploaded_at": repo.uploaded_at,

                "chat_count": repo.sessions.count()

            })

        return Response(data)
    

class RepositoryStatsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, repository_id):

        repo = Repository.objects.get(

            id=repository_id,

            user=request.user

        )

        session_count = repo.sessions.count()

        message_count = ChatMessage.objects.filter(

            session__repository=repo

        ).count()

        recent_chats = ChatSession.objects.filter(
            repository=repo
        ).order_by("-created_at")[:5]

        return Response({

            "repository": repo.name,

            "github_url": repo.github_url,

            "uploaded_at": repo.uploaded_at,

            "chat_sessions": session_count,

            "messages": message_count,

            "recent_chats": [

                {

                    "id": chat.id,

                    "title": chat.title

                }

                for chat in recent_chats

            ]

        })
    

class DeleteRepositoryAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, repository_id):

        repository = Repository.objects.get(

            id=repository_id,

            user=request.user

        )
        repo_name = repository.name

        try:

            db = ChromaVectorStore(
                collection_name=repo_name
            )

            db.delete_collection()

            print(f"Deleted Chroma collection: {repo_name}")

        except Exception as e:

            print(e)

        repo_path = os.path.join(
            "repositories",
            repo_name
        )

        if os.path.exists(repo_path):

            shutil.rmtree(repo_path)

        # Delete database record
        repository.delete()

        return Response({

            "message":"Repository deleted successfully."

        },
        status=status.HTTP_200_OK
        )