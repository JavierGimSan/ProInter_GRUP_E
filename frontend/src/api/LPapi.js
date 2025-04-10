import axios from "axios";
import { BACKEND_URL } from "../config/constansts";

export class LPapi {

    static api = axios.create({
        baseURL: BACKEND_URL
    });

    static async queryChat(query) {
        const encodedQuery = encodeURI(query);
        return LPapi.api.get(`/chat?query=4${encodedQuery}`);
    }
}