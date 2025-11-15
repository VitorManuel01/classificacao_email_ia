import {createContext, useState, ReactNode} from "react";

import { UserData } from "@/interface/UserData";

interface UserContextProps {
    userData: UserData | null;
    setUserData: (data: UserData) => void;
}

export const UserContext = createContext<UserContextProps>({
    userData: null,
    setUserData: () => {},
});

export const UserProvider = ({ children }: { children: ReactNode }) => {
    const [userData, setUserData] = useState<UserData | null>(null);

    return (
        <UserContext.Provider value={{ userData, setUserData }}>
            {children}
        </UserContext.Provider>
    );
};