import { useEffect, useRef } from "react";
import mermaid from "mermaid";

mermaid.initialize({
    startOnLoad: false,
    theme: "default",
    securityLevel: "loose"
});

export default function MermaidDiagram({ chart }) {

    const ref = useRef(null);

    useEffect(() => {

        if (!chart) return;

        const id = "mermaid-" + Math.random().toString(36).slice(2);

        mermaid
            .render(id, chart)
            .then(({ svg }) => {
                if (ref.current) {
                    ref.current.innerHTML = svg;
                }
            });

    }, [chart]);

    return <div className="mermaid-diagram" ref={ref} />;
}