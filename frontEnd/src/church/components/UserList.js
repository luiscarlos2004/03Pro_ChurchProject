import React from "react";
import { getListUsers } from "../../helpers/getListUsers";

export const UserListsomething = (publisher) => {
    const argspeople = {
        "id":publisher.children[0],
        "email":publisher.children[3]
    }
    return (
        <>
            <h1>Something</h1>
            <ul>
                <li>{argspeople["id"]}</li>
                <li>{argspeople["email"]}</li>
            </ul>
        </>
        
    )
}