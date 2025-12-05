import axios from "axios";
import { getCsrfToken } from "./csrfTokenUtils";


export async function checkUserStatus(status){
    let statusURL = 'http://localhost:8000/users/check-status'
    console.log('print 1');
    
    try {
        console.log('print 2');
        const response = await axios.get(`${statusURL}`, {
            withCredentials: true,
            headers: {
            "X-CSRFToken": getCsrfToken()
            }
        })
        console.log('print 3');
        console.log('response: ',response);
        if (response.status === 200) {
            console.log('print 4');
            
            let isLoggedin = response.data.logged_in;
            let isAdmin = response.data.is_superuser;
        
            status.isLoggedin = isLoggedin;
            status.isAdmin = isAdmin;
            
        console.log('status: ', status.isLoggedin, status.isAdmin);
        // return status;
    }
    } catch (error) {
        console.error(error)
        return 'Something wrong happened'
    }
}
