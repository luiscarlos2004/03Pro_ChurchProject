import React from "react";
import { getListUsers } from "../../helpers/getListUsers";

export const UserListsomething = (publisher) => {
    // const users = getListUsers( publisher );
    
    // console.log(publisher.children)
    const args = {
        "id":publisher.children[0],
        "email":publisher.children[3]
    }
    return (
        <>
            <h1>Something</h1>
            <ul>
                <li>{args["id"]}</li>
                <li>{args["email"]}</li>
            </ul>
        </>
        
    )
}