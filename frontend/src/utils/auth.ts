export const isAuthenticated = (): boolean => {
    const token = localStorage.getItem("token") || localStorage.getItem("authToken");
    
    return !!token;
};
