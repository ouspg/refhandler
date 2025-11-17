import { Navigate, Outlet } from "react-router-dom";
import { useUserStore } from "../../store/userStore";

interface ProtectedRouteProps {
  requireAuth?: boolean;
  children?: React.ReactNode;
  allowedRoles?: string[];
}

const ProtectedRoute = ({ allowedRoles = [], requireAuth = true, children }: ProtectedRouteProps) => {
  const { user } = useUserStore();
  console.log(user);
  if (requireAuth && !user?.token || !allowedRoles?.includes(user?.role || '')) {
    return <Navigate to="/login" replace />;
  }
  return children || <Outlet />;
};

export default ProtectedRoute;