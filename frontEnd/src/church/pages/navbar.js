import { Link } from "react-router-dom";

export const Navbar = () => {
    return(
        <>
            <nav>
                <ul>
                    <li><Link to='/home'>Home</Link></li>
                    <li><Link to='/userslist'>Users</Link></li>
                </ul>
            </nav>
        </>
    )
}