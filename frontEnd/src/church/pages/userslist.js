import axios from "axios"
import { useEffect, useState } from "react";
import { getListUsers } from "../../helpers/getListUsers";
import {UserListsomething} from "../components/UserList";
const baseUrl = "http://127.0.0.1:5000";

export const UserList = () => {
    const [people,setpeople] = useState([]);
    const handlesubmit  =  async() => {
        try{
            const data  = await axios.get(`${baseUrl}/people`,)
            setpeople(data.data)
        }catch(err){
            console.error(err);
        }
    }
    
    useEffect(()=>{
        handlesubmit()
    },[])
    return(
        <>
            <h1>User List</h1>
            <ul>
                {
                    people.map(user => (
                        <UserListsomething key={user[0]}>{user}</UserListsomething>
                    ))
                }
            </ul>
        </>
    )
}