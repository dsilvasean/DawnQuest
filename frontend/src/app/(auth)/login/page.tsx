'use client';
import React, { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "react-toastify";
import Loader from "@/components/Loader";
import FormCard from "@/components/FormCard";
import { useRouter } from "next/navigation";


const Login = () => {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = async(e:React.FormEvent)=>{
        e.preventDefault();
        const payload = {
            email,
            password
        };
        try{
            setLoading(true);
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/token/`, {
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify(payload),
            });

            const data = await response.json();
            if(response.ok){
                const { access, refresh } = data;
                if(!access || !refresh){
                    toast.error("Invalud token response");
                    return;
                }          
                localStorage.setItem("access_token", access);
                localStorage.setItem("refresh_token", refresh);
                toast.success("Login Successfull!");

                const timeout = setTimeout(()=>{
                    router.push("/dashboard")
                }, 3500)
            }
            else{
                toast.error(data.detail)
            }
        }
        catch (error){
            toast.error("Server Error")
        }
        finally{
            setLoading(false)
        }
    }

  return (
    <>
        <Loader loading={loading} fullScreen/>
        <FormCard title="Login Student" onSubmit={handleSubmit} loading={loading} buttonText="Login">
            <div className="grid gap-3">
                <Label>Email</Label>
                <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="john@mail.com" className="focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2" />
                <Label>Password</Label>
                <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" className="focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2" />

            </div>
        </FormCard>
    </>
  )
}

export default Login