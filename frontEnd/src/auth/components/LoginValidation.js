
import axios from "axios";
import { useState } from "react";
import { AuthContex } from "../context/AuthContext";
import {useContext} from 'react';
import { types } from "../types/types";
import { useNavigate } from 'react-router-dom';


const baseUrl = "http://127.0.0.1:5000";


export const LoginValidation = () => {
    const navigate = useNavigate();

    const[username, setUsername] = useState();
    const[password, setPassword] = useState();

    const {login,state} = useContext(AuthContex);

    const handleChangeUsername = (e, field) => {
        if(field == 'username'){
            setUsername(e.target.value);
        }else if(field == 'password'){
            setPassword(e.target.value);
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault();

        if(!username){
            alert('username required');
            return
        }
        if(!password){
            alert('Password required');
            return
        }
        try{
            const data = await axios.post(`${baseUrl}/auth/login`, { username:username, password:password });
            
            if(data.data === "True"){

                login(username.username,types.login);
                navigate('/home');

            }else{

                login(username.username,types.logout);
                navigate('/signup');
            }

        }catch(err){
            console.error(err.message)
        }
    }

    // const validate = () => {
        
    // }

    return(
        <>

            <form onSubmit={handleSubmit}>

                <label htmlFor="username">Username</label>
                <input onChange={(e)=>handleChangeUsername(e,"username")} type="text" name="username" id="username"/>
                <label htmlFor="password">Password</label>
                <input onChange={(e)=>handleChangeUsername(e,"password")} type="password" name="password" id="password"/>
                <button type="submit">Submit</button>
            
            </form>

        </>
    )
}

