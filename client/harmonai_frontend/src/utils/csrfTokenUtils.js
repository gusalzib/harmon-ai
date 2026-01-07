/**
 * Authors of code:
 * - 
 */

export function getCsrfToken() {

    // this creates an array of the all cookies in the cookie storage of the broswer
    const cookies = document.cookie.split(';');

    // selecting the cookie that starts with csrftoken
    const csrfCookie = cookies.find(cookie => cookie.trim().startsWith('csrftoken'));

    // debug print
    console.log('printing th csrfCookie in UTILS ', csrfCookie);

    if (csrfCookie) {
        // the cookie with the shape: csrftoken=vWnnFs3w2nYNp1lpD8yequrnZ6ApEUJ4
        // we split at '=' to get the actual value
        const token = csrfCookie.split('=')[1];
        return token;
    }
    
    // if we reach here then the cookie was not found. we return null
    return null; 

}

