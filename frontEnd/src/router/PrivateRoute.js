import {useContext} from 'react';
import { Navigate } from 'react-router-dom';
import {AuthContex} from '../auth';

export const PrivateRoute = ({children}) => {
    
    const {state} = useContext( AuthContex );
    // console.log(state.logged)
    return(state.logged)
        ? children 
        : <Navigate to="/login"/>
}