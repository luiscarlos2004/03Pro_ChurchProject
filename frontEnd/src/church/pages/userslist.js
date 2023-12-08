import axios from "axios"
import { useEffect, useState } from "react";
import { getListUsers } from "../../helpers/getListUsers";
import {UserListsomething} from "../components/UserList";
const baseUrl = "http://127.0.0.1:5000";

export const UserList = () => {
    const [people,setpeople] = useState([]);
    const handlesubmit  =  async() => {
        // e.preventDefault();
       
        try{
            const data  = await axios.get(`${baseUrl}/people`,)
            // console.log(data.data)
            setpeople(data.data)
            // getListUsers(events)
            // console.log(events);
            // return events.map(event => {
            //     console.log(event)
            // })
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
                        // args= {
                        //     "name":user[3]
                        // }
                        // console.log(user[3])
                        <UserListsomething key={user[0]}>{user}</UserListsomething>
                    ))
                }
            </ul>
        </>
    )
}