'use client';

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/authService';
import toast from 'react-hot-toast';

const Navbar = () => {
  const router = useRouter();
  const [isOpen, setIsOpen] = React.useState(false);

  const handleLogout = () => {
    authService.logout();
    toast.success('Logged out successfully');
    router.push('/login');
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link href="/dashboard" className="text-xl font-bold">
            Metrology Checker
          </Link>

          <div className="hidden md:flex space-x-6">
            <Link href="/dashboard" className="hover:text-blue-200 transition">
              Dashboard
            </Link>
            <Link href="/upload" className="hover:text-blue-200 transition">
              Upload
            </Link>
            <Link href="/products" className="hover:text-blue-200 transition">
              Products
            </Link>
          </div>

          <button
            onClick={handleLogout}
            className="bg-red-600 px-4 py-2 rounded-lg hover:bg-red-700 transition"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
