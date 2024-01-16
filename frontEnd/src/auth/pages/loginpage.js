

import { LoginValidation } from "../components/LoginValidation"
import "../static/style.css";

export const LoginPage = () => {
    return( 
        <div className="loginmain">
            <h1 className="logintitle">Login</h1>
            
            <LoginValidation/>
            {/* <button onClick={}>Sign up</button> */}
        </div>
    )
}
