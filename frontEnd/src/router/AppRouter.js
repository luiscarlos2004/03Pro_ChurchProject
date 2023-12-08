import {Route, Routes} from 'react-router-dom';
import { LoginPage } from '../auth/pages/loginpage';
import { SignuPage } from '../auth/pages/signupage';
import { HeroesRoutes } from '../church/routes/HeroesRoutes';
import { PrivateRoute } from './PrivateRoute';
import { AuthProvider } from "../auth/context/AuthProvider";
import { Navbar } from "../church/pages/navbar";


export const AppRouter = () => {
    return (
        <AuthProvider>
            <Routes>
                <Route path="login" element={<LoginPage/>}/>
                <Route path="signup" element={<SignuPage/>}/>
                <Route path='/*' element={
                    <PrivateRoute>
                        <Navbar/>
                        <HeroesRoutes/>
                    </PrivateRoute>
                }/>
            </Routes>
        </AuthProvider>
    )
}
