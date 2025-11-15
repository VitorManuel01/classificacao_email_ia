"use client"

import React, {useState, useContext} from "react";
import {UserContext} from "@/context/UserContext"
import {UserData} from '@/interface/UserData'
import styles from './UserInfo.module.css'

const UserInfo = ({onNext}: { onNext: () => void }) => {
    const {setUserData} = useContext(UserContext); // access the setUserData function from context
    const [formData, setFormData] = useState<UserData>({
        fullName: "",
        email: ""
    }); // State to hold form data
    const [errors, setErrors] = useState<Partial<UserData>>({}); // state to hold validation errors

    const validateForm = (): boolean => {
        const newErrors: Partial<UserData> = {};

        if (!formData.fullName.trim()) {
            newErrors.fullName = "Nome completo é obrigatório";
        }
        if (!formData.email.trim()) {
            newErrors.email = "Email é obrigatório";
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = "Email inválido";
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    }; //validation function so that all fields are filled correctly to proceed to analysis form

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (validateForm()) {
            setUserData(formData);
            onNext();
        }
    };//handle form submission that validates and sets user data in context then calls onNext to proceed

    return (
        <div className={styles.container}>
            <div className={styles.card}>
                <h2 className={styles.title}>Informações de Contato</h2>
                <p className={styles.subtitle}>
                    Preencha seus dados para continuar
                </p>

                <form onSubmit={handleSubmit} className={styles.form}>

                    <div className={styles.formGroup}>
                        <label htmlFor="fullName" className={styles.label}>
                            Nome Completo
                        </label>
                        <input
                            id="fullName"
                            type="text"
                            className={`${styles.input} ${errors.fullName ? styles.inputError : ''}`}
                            value={formData.fullName}
                            onChange={(e) => setFormData({...formData, fullName: e.target.value})}
                            placeholder="Digite seu nome completo"
                        />
                        {errors.fullName && (
                            <span className={styles.error}>{errors.fullName}</span>
                        )}
                    </div>

                    <div className={styles.formGroup}>
                        <label htmlFor="email" className={styles.label}>
                            Email
                        </label>
                        <input
                            id="email"
                            type="email"
                            className={`${styles.input} ${errors.email ? styles.inputError : ''}`}
                            value={formData.email}
                            onChange={(e) => setFormData({...formData, email: e.target.value})}
                            placeholder="seu@email.com"
                        />
                        {errors.email && (
                            <span className={styles.error}>{errors.email}</span>
                        )}
                    </div>

                    <button type="submit" className={styles.submitButton}>
                        Continuar
                    </button>
                </form>
            </div>
        </div>
    );
}

export default UserInfo;