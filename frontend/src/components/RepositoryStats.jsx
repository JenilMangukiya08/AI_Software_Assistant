export default function RepositoryStats({ stats }) {

    return (

        <div className="stats-card">

            <h3>Repository Statistics</h3>

            <p>🐍 Python : {stats.python}</p>

            <p>📄 Markdown : {stats.markdown}</p>

            <p>📦 JSON : {stats.json}</p>

            <p>⚙ YAML : {stats.yaml}</p>

            <p>📚 Documents : {stats.documents}</p>

            <p>🧩 Chunks : {stats.chunks}</p>

        </div>

    )

}