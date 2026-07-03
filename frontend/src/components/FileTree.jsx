export default function FileTree({
    tree,
    onSelect
}){

    return (

        <div className="file-tree">

            {
                Object.entries(tree).map(
                    ([name,value])=>{

                        if(value===null){

                            return(

                                <div
                                key={name}
                                className="file-item"
                                onClick={()=>
                                    onSelect(name)
                                }
                                >

                                    <span className="file-icon">📄</span>
                                    <span className="file-name">{name}</span>

                                </div>

                            )

                        }

                        return(

                            <details key={name} className="folder">

                                <summary className="folder-name">

                                    <span className="folder-icon">📂</span>
                                    <span className="folder-label">{name}</span>

                                </summary>

                                <FileTree
                                    tree={value}
                                    onSelect={onSelect}
                                />

                            </details>

                        )

                    }
                )
            }

        </div>

    )

}