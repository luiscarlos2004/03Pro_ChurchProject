import { Outlet, Link } from "react-router-dom"

export const Layout = () => {
    return(
        <>
            <nav>
                <ul>
                    <li>
                        <Link to="/">Home</Link>
                    </li>
                    <li>
                        <Link to="/login">Login</Link>
                    </li>
                    <li>
                        <Link to="/signup">Login</Link>
                    </li>
                </ul>
            </nav>
            <Outlet/>
        </>
    )
}

// export default Layout;