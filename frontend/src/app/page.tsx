"use client";
import Image from "next/image";
import React, {useState} from "react";
import UserInfo from "@/components/userInfo";
import EmailAnalysisForm from "@/components/EmailAnalysisForm";

export default function Home() {
    const [step, setStep] = useState<"userInfo" | "emailForm">("userInfo");


  return (
      <div>
            {step === "userInfo" && <UserInfo onNext={() => setStep("emailForm")} />}
            {step === "emailForm" && <EmailAnalysisForm />}
      </div>
  );
}
