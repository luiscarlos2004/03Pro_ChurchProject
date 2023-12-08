import { BrowserRouter } from "react-router-dom";
import { AppRouter } from "./router/AppRouter";


export const ChurchApp = () => { 
    return(
        <BrowserRouter>
            <AppRouter/>
        </BrowserRouter>
        
    )
}