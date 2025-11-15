"use client";

import {createContext, useState, ReactNode} from "react";

import { UserData } from "@/interface/UserData";

// Define the props of the context using the UserData interface
interface UserContextProps {
    userData: UserData | null;
    setUserData: (data: UserData) => void;
}

//create the context with default values to be used in the provider and consumer components
export const UserContext = createContext<UserContextProps>({
    userData: null,
    setUserData: () => {},
});

//defining the provider component that will wrap the parts of the app that need access to the user data
export const UserProvider = ({ children }: { children: ReactNode }) => {
    const [userData, setUserData] = useState<UserData | null>(null);

    return (
        <UserContext.Provider value={{ userData, setUserData }}>
            {children}
        </UserContext.Provider>
    );
};