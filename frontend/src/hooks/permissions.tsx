import { useEffect, useState } from "react";

export const usePermissions = () => {
  const [permissions, setPermissions] = useState<string[]>([]);

  useEffect(() => {
    const stored = localStorage.getItem("permissions");
    if (stored) {
      setPermissions(JSON.parse(stored));
    }
  }, []);

  const hasPermission = (permission: string) => {
    return permissions.includes(permission);
  };

  const hasPermissions = (required: string[]) => {
    return required.every((p) => permissions.includes(p));
  };

  const setNewPermissions = (newPermissions: string[]) => {
    setPermissions(newPermissions);
    localStorage.setItem("permissions", JSON.stringify(newPermissions));
  };

  return { permissions, hasPermission, hasPermissions, setNewPermissions };
};
