import { useState } from "react"
import { LPapi } from "../../api/LPapi";

export const Chat = () => {

    const [messages, setMessages] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const query = e.target?.[0]?.value || "";
        if (!query) return;

        const response = await LPapi.queryChat(query);
        console.log(response);
    }

    return (
        <main>
            <h1>Chat</h1>

            <section>
                {}
            </section>

            <form onSubmit={handleSubmit}>
                <textarea placeholder="Escribe algo..."></textarea>
                <button type="submit">Send</button>
            </form>
        </main>
    )
}