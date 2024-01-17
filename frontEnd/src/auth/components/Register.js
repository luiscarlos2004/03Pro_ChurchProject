import axios from "axios";
import { useState } from "react";



export const Register = () => {
    const baseUrl = "http://127.0.0.1:5000";

    const[username,setUsername] = useState();
    const[password,setPassword] = useState();
    const[fullname, setFullname] = useState();

    const handleChangeUsername = (e,field) => {
        
        if(field == 'username'){
            setUsername(e.target.value);
        }else if(field == 'password'){
            setPassword(e.target.value);
        }else if(field == 'fullname'){
            setFullname(e.target.value)
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
        if(!fullname){
            alert('Username required');
            return
        }
        try{
            const data = await axios.post(`${baseUrl}/auth/register`,{username:username,password:password,fullname:fullname});
            console.log(data)
        }catch(err){
            console.error(err.message);
        }
    }
    return(
        <>
            <form onSubmit={handleSubmit}>
                <label htmlFor="username">Username</label>
                <input onChange={(e)=>handleChangeUsername(e,"username")} type="text" name="username" id="username"/>
                <label htmlFor="password">Password</label>
                <input onChange={(e)=>handleChangeUsername(e,"password")} type="password" name="password" id="password"/>
                <label htmlFor="fullname">Fullname</label>
                <input onChange={(e)=>handleChangeUsername(e,"fullname")} type="text" name="fullname" id="fullname"/>
                <button type="submit">Submit</button>
            </form>
        </>
    )
}