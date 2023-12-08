import { Routes, Route } from 'react-router-dom';
import {Home} from '../pages/home';
import { UserList } from '../pages/userslist';

export const HeroesRoutes = () => {
    return(
        <Routes>
            <Route path="home" element={<Home/>}/>
            <Route path="userslist" element={<UserList/>}/>
        </Routes>
    )
}