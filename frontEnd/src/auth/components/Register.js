import axios from "axios";
import { useState } from "react";



export const Register = () => {
    const baseUrl = "http://127.0.0.1:5000";

    const[type_document, setType_document] = useState();
    const[document, setDocument] = useState();
    const[first_name, setFirst_name] = useState();
    const[middle_name, setMiddle_name] = useState();
    const[first_last_name, setFirst_last_name] = useState();
    const[second_last_name, setSecond_last_name] = useState();
    const[address, setAddress] = useState();
    const[cellphone, setCellphone] = useState();
    const[email,setEmail] = useState();
    const[company_id, setCompany_id] = useState();

    const[username,setUsername] = useState();
    const[password,setPassword] = useState();

    const handleChangeUsername = (e,field) => {
        
        if(field == 'type_document'){
            setType_document(e.target.value);
        }else if(field == 'document'){
            setDocument(e.target.value);
        }else if(field == 'first_name'){
            setFirst_name(e.target.value)
        }else if(field == 'middle_name'){
            setMiddle_name(e.target.value)
        }else if(field == 'first_last_name'){
            setFirst_last_name(e.target.value)
        }else if(field == 'second_last_name'){
            setSecond_last_name(e.target.value)
        }else if(field == 'address'){
            setAddress(e.target.value)
        }else if(field == 'cellphone'){
            setCellphone(e.target.value)
        }else if(field == 'email'){
            setEmail(e.target.value)
        }else if(field == 'company_id'){
            setCompany_id(e.target.value)
        }else if(field == 'username'){
            setUsername(e.target.value)
        }else if(field == 'password'){
            setPassword(e.target.value)
        }
        

    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        if(!type_document){
            alert('Type_document required');
            return
        }
        if(!document){
            alert('Document required');
            return
        }
        if(!first_name){
            alert('First_name required');
            return
        }
        // if(!middle_name){
        //     alert('middle_name required');
        //     return
        // }
        if(!first_last_name){
            alert('first_last_name required');
            return
        }
        // if(!second_last_name){
        //     alert('second_last_name required');
        //     return
        // }
        if(!address){
            alert('address required');
            return
        }
        if(!cellphone){
            alert('cellphone required');
            return
        }
        if(!email){
            alert('email required');
            return
        }
        if(!company_id){
            alert('company_id required');
            return
        }
        if(!username){
            alert('username required');
            return
        }
        if(!password){
            alert('password required');
            return
        }
        
        try{
            const data = await axios.post(`${baseUrl}/auth/registerperson`,{type_document:type_document,document:document,first_name:first_name,middle_name:middle_name,first_last_name:first_last_name,second_last_name:second_last_name,address:address,cellphone:cellphone,email:email,company_id:company_id,username:username,password:password});
            console.log(data)
        }catch(err){
            console.error(err.message);
        }
    }
    return(
        <>
            <form onSubmit={handleSubmit}>
                <label htmlFor="type_document">Type_document</label>
                <input onChange={(e)=>handleChangeUsername(e,"type_document")} type="text" name="type_document" id="type_document"/>
                <label htmlFor="document">Document</label>
                <input onChange={(e)=>handleChangeUsername(e,"document")} type="text" name="document" id="document"/>
                <label htmlFor="first_name">First_name</label>
                <input onChange={(e)=>handleChangeUsername(e,"first_name")} type="text" name="first_name" id="first_name"/>
                <label htmlFor="middle_name">Middle_name</label>
                <input onChange={(e)=>handleChangeUsername(e,"middle_name")} type="text" name="middle_name" id="middle_name"/>
                <label htmlFor="first_last_name">First last name</label>
                <input onChange={(e)=>handleChangeUsername(e,"first_last_name")} type="text" name="first_last_name" id="first_last_name"/>
                <label htmlFor="second_last_name">Second last name</label>
                <input onChange={(e)=>handleChangeUsername(e,"second_last_name")} type="text" name="second_last_name" id="second_last_name"/>
                <label htmlFor="address">Address</label>
                <input onChange={(e)=>handleChangeUsername(e,"address")} type="text" name="address" id="address"/>
                <label htmlFor="cellphone">Cellphone</label>
                <input onChange={(e)=>handleChangeUsername(e,"cellphone")} type="number" name="cellphone" id="cellphone"/>
                <label htmlFor="email">Email</label>
                <input onChange={(e)=>handleChangeUsername(e,"email")} type="email" name="email" id="email"/>
                <label htmlFor="company_id">Company id</label>
                <input onChange={(e)=>handleChangeUsername(e,"company_id")} type="number" name="company_id" id="company_id"/>
                <label htmlFor="username">Username</label>
                <input onChange={(e)=>handleChangeUsername(e,"username")} type="text" name="username" id="username"/>
                <label htmlFor="password">Password</label>
                <input onChange={(e)=>handleChangeUsername(e,"password")} type="password" name="password" id="password"/>
                <button type="submit">Submit</button>
            </form>
        </>
    )
}