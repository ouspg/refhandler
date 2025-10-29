import { Navigate, Outlet } from "react-router-dom";
import { isAuthenticated } from "../../utils/auth";

interface ProtectedRouteProps {
  requireAuth?: boolean;
}

const ProtectedRoute = ({ requireAuth = true }: ProtectedRouteProps) => {
  if (requireAuth && !isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  if (!requireAuth && isAuthenticated()) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;