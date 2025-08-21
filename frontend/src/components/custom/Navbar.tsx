'use client'

import Link from "next/link"
import { Menu } from "lucide-react"
import { useState } from "react"
import { Button } from "@/components/ui/button"

export default function Navbar() {

  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <nav className="z-10 sticky top-0 px-6 py-5 bg-white shadow-md border-b">
      <div className="grid grid-cols-3 items-center">
        <div className="text-xl font-bold">
          <Link className="font-courgette-regular text-4xl" href="/">
            <span className="text-brand">Dawn</span>
          </Link>
        </div>

        <div className="hidden md:flex justify-center gap-10 font-poppins-regular text-xl font-extrabold text-gray-700">
          <Link className="hover:text-brand active:brand" href="/">Learning Center</Link>
          <Link className="hover:text-brand active:brand" href="/">Acca Tutor</Link>
          <Link className="hover:text-brand active:brand" href="/login">Login</Link>
          <Link className="hover:text-brand active:brand" href="/register">Signup</Link>


        </div>
        

        <div className="flex justify-end md:hidden">
          <Button variant="ghost" size="icon" onClick={() => setMenuOpen(!menuOpen)}>
            <Menu className="w-6 h-6" />
          </Button>
        </div>
      </div>

      {menuOpen && (
        <div className="mt-4 flex flex-col items-center gap-4 font-poppins-regular text-lg md:hidden">
          <Link href="/">Learning Center</Link>
          <Link href="/">Acca Tutor</Link>
          <Link href="/">Login</Link>


        </div>
      )}
    </nav>
  )
}
