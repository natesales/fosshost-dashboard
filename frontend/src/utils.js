import {Project, SnackBars, Page} from "./stores";

export function addSnackbar(status, message, color, timeout) {
    let id = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5);
    SnackBars.update(sb => {sb[id] = {status, message, color, timeout}; return sb})
}

// Check if we're already logged in
export function checkLogin(page) {
    if (page === "index" || page === "login") {
        fetch("/api/auth/check", {
            credentials: "include"
        })
            .then(response => response.json())
            .then(data => {
                if (data["success"]) {
                    Project.set(data["message"])
                    Page.set("dashboard")
                } else {
                    Page.set("login")
                }
            })
    }
}

export function logOut() {
    fetch("/api/auth/logout", {
        credentials: "include"
    })
        .then(response => response.json())
        .then(data => Page.set("index"))
}
