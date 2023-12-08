import { useContext } from "react"
import { AuthContex } from "../../auth"

export const Home = () => {
    const{logout} = useContext(AuthContex);
    return(
        <>
            <h1>Home</h1>
            <button onClick={()=>logout()}>logout</button>
        </>
    )
}