// components/AuthCard.tsx
"use client";
import React from "react";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import Image from "next/image";

interface FormCardProps {
  title: string;
  children: React.ReactNode;
  onSubmit: (e: React.FormEvent) => void;
  loading?: boolean;
  buttonText?: string;
}

const FormCard: React.FC<FormCardProps> = ({ title, children, onSubmit, loading, buttonText = "Submit" }) => {
  return (
    <div className="flex justify-center items-center h-screen">
      <form onSubmit={onSubmit}>
        <Card className="w-[350px] shadow-2xl border-2">
          <CardHeader className="text-center relative pt-16">
            <div className="absolute -top-20 left-1/2 transform -translate-x-1/2">
              <Image
                src="/brand_logo.png"
                alt="brand_logo"
                width={160}
                height={160}
                className="rounded-full shadow-lg"
              />
            </div>
            <span className="mt-4 block text-lg font-semibold">{title}</span>
          </CardHeader>
          <CardContent>{children}</CardContent>
          <CardFooter className="flex justify-center">
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-brand font-bold text-white py-2 px-4 rounded hover:bg-brand-active"
            >
              {loading ? "Processing..." : buttonText}
            </button>
          </CardFooter>
        </Card>
      </form>
    </div>
  );
};

export default FormCard;
