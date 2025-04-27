import { useEffect } from "react";
import { useAuth } from "../contexts/useAuth";
import { useNavigate, useLocation } from "react-router-dom";
import { Spinner } from "@chakra-ui/react";

const PrivateRoute = ({ children }) => {
    const { isAuthenticated, loading,user } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    console.log("isauth",isAuthenticated,'loading',loading,"user:",user)

    useEffect(() => {
        if (!loading && !isAuthenticated) {
            navigate('/login', { state: { from: location } });
        }
    }, [loading, isAuthenticated, navigate, location]);

    if (loading) {
        return <Spinner size="xl" />;
    }

    return isAuthenticated ? children : null;
};

export default PrivateRoute;