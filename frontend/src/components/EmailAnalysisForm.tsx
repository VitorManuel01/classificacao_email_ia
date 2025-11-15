"use client";
import React, {useState, useContext, useRef} from "react";
import {UserContext} from "@/context/UserContext";
import {useRouter} from "next/navigation";
import {UserData} from "@/interface/UserData";
import styles from "./EmailAnalysisForm.module.css";

type AnalysisResponse = {
    classification: string;
    suggestedResponse: string;
};

export default function EmailAnalysisForm() {
    const {userData} = useContext(UserContext);
    const router = useRouter();
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [emailText, setEmailText] = useState<string>("");
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [result, setResult] = useState<AnalysisResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    if (!userData) { //simple check to ensure user data is present before rendering the form
        return (
            <div className={styles.container}>
                <div className={styles.card}>
                    <h2 className={styles.title}>Acesso Negado</h2>
                    <p className={styles.subtitle}>
                        Por favor, forneça suas informações antes de acessar a análise de emails.
                    </p>
                    <button onClick={() => router.push("/")} className={styles.submitButton}>
                        Voltar
                    </button>
                </div>
            </div>
        );
    }

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setError(null);
        const selectedFile = e.target.files?.[0] || null;
        setFile(selectedFile);
    }; //file input change handler to update state when a file is selected

    const handleFileButtonClick = () => {
        fileInputRef.current?.click();
    }; //trigger file input click when custom button is clicked

    const handleRemoveFile = () => {
        setFile(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };// remove selected file and reset file input

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setResult(null);

        if (!emailText.trim() && !file) {
            setError("Por favor, cole o texto do email ou envie um arquivo.");
            return;
        }

        setLoading(true);
        try {
            const formData = new FormData();
            const API_URL = process.env.NEXT_PUBLIC_API_URL;
            formData.append("userData", JSON.stringify(userData as UserData));
            if (emailText.trim()) formData.append("email_text", emailText);
            if (file) formData.append("file", file);

            const response = await fetch(`${API_URL}/analyze_email`, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(errorText || "Erro ao analisar email.");
            }
            //sending everything need to backend for the AI to analyse and get the response to show to user
            const data: AnalysisResponse = await response.json();
            setResult(data);
        } catch (err: any) {
            setError(err.message || "Erro ao analisar email.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.container}>
            <div className={styles.card}>
                <h2 className={styles.title}>Análise de Email</h2>
                <p className={styles.subtitle}>Olá, {userData.fullName}</p>

                <form onSubmit={handleSubmit} className={styles.form} noValidate>
                    <div className={styles.formGroup}>
                        <label htmlFor="emailText">Texto do Email</label>
                        <textarea
                            id="emailText"
                            value={emailText}
                            onChange={(e) => setEmailText(e.target.value)}
                            rows={10}
                            placeholder="Cole o texto do email aqui..."
                            className={error && !file && !emailText.trim() ? styles.inputError : undefined}
                            aria-invalid={Boolean(error && !file && !emailText.trim())}
                            aria-describedby={error && !file && !emailText.trim() ? "emailText-error" : undefined}
                        />
                        <span className={styles.helper}>
                                    Você pode colar o conteúdo ou enviar um arquivo abaixo.
                                </span>
                        {error && !file && !emailText.trim() && (
                            <span id="emailText-error" className={styles.error}>
                                        {error}
                                    </span>
                        )}
                    </div>

                    <div className={styles.formGroup}>
                        <label htmlFor="fileUpload">Anexar Arquivo</label>
                        <input
                            ref={fileInputRef}
                            id="fileUpload"
                            type="file"
                            accept=".txt,.pdf,application/pdf,text/plain"
                            onChange={handleFileChange}
                            className={styles.fileInput}
                        />
                        <button
                            type="button"
                            onClick={handleFileButtonClick}
                            className={styles.fileButton}
                        >
                            <svg
                                className={styles.fileIcon}
                                fill="none"
                                stroke="currentColor"
                                viewBox="0 0 24 24"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                                />
                            </svg>
                            Escolher Arquivo
                        </button>
                        {file && (
                            <div className={styles.filePreview}>
                                <svg
                                    className={styles.filePreviewIcon}
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                    xmlns="http://www.w3.org/2000/svg"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                                    />
                                </svg>
                                <span className={styles.fileName}>{file.name}</span>
                                <button
                                    type="button"
                                    onClick={handleRemoveFile}
                                    className={styles.removeButton}
                                    aria-label="Remover arquivo"
                                >
                                    <svg
                                        fill="none"
                                        stroke="currentColor"
                                        viewBox="0 0 24 24"
                                        xmlns="http://www.w3.org/2000/svg"
                                    >
                                        <path
                                            strokeLinecap="round"
                                            strokeLinejoin="round"
                                            strokeWidth={2}
                                            d="M6 18L18 6M6 6l12 12"
                                        />
                                    </svg>
                                </button>
                            </div>
                        )}
                        <span className={styles.helper}>Formatos aceitos: TXT, PDF</span>
                    </div>

                    <button type="submit" className={styles.submitButton} disabled={loading}>
                        {loading ? "Analisando..." : "Enviar para Análise"}
                    </button>
                </form>

                {error && (file || emailText.trim()) && (
                    <div className={styles.errorAlert}>{error}</div>
                )}

                {result && (
                    <div className={styles.resultSection}>
                        <h3 className={styles.resultTitle}>Resultado da Análise</h3>
                        <div className={styles.resultItem}>
                            <span className={styles.resultLabel}>Classificação:</span>
                            <span className={styles.resultValue}>{result.classification}</span>
                        </div>
                        <div className={styles.resultItem}>
                            <span className={styles.resultLabel}>Resposta Sugerida:</span>
                        </div>
                        <div className={styles.resultBox}>{result.suggestedResponse}</div>
                    </div>
                )}
            </div>
        </div>
    );
}