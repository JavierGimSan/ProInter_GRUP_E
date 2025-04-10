import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Home } from "./pages/home/page";
import { Chat } from "./pages/chat/page";
import { Layout } from "./Layout";

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="chat" element={<Chat />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
