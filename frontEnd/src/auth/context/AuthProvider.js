import { useReducer, useState } from "react";
import { AuthContex } from "./AuthContext";
import { authReducer } from "./authReducer";
import { types } from "../types/types";

// const initialState = {
//     logged: false
// }

const init = () => {
    const user = JSON.parse(localStorage.getItem('user'));
    return{
        logged:!!user,//this is for check if exist
        user,
    }
}

export const AuthProvider = ({ children }) => {
    const [state, dispatch] = useReducer( authReducer, {}, init );
    // const [statelogin, setStateLogin] = useState()
    const login = (name = '',value) => {
        
        const user = {id:'ABC',name};
        const action = {
            type:value,
            payload:user
        }
        localStorage.setItem('user', JSON.stringify(user));
        dispatch(action);
    }

    const logout = () => {
        localStorage.removeItem('user');
        const action = {type:types.logout}
        dispatch(action);
    }
    return(
        <AuthContex.Provider value={{login:login,state , logout:logout}}>
            {children}
        </AuthContex.Provider>
    );
}