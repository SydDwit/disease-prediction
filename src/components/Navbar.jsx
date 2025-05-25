import React, { useState } from "react";
import { Menu, X, LogOut } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const username = localStorage.getItem('username');
  const isAdmin = localStorage.getItem('isAdmin') === 'true';

  const toggleMenu = () => setMenuOpen(!menuOpen);

  const handleLogout = () => {
    localStorage.removeItem('username');
    localStorage.removeItem('isAdmin');
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-md fixed w-full z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16">
        <Link to={isAdmin ? "/admin/dashboard" : "/home"} className="text-xl font-bold text-blue-600">
          {isAdmin ? "Admin Dashboard" : "Prediction"}
        </Link>
        
        <div className="hidden md:flex items-center space-x-6">
          {!isAdmin && (
            <>
              <Link to="/home" className="text-gray-700 hover:text-blue-600">
                Home
              </Link>
              <Link to="/contact" className="text-gray-700 hover:text-blue-600">
                Contact
              </Link>
            </>
          )}
          
          {username ? (
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {username}</span>
              <button
                onClick={handleLogout}
                className="flex items-center text-gray-700 hover:text-blue-600"
              >
                <LogOut className="w-4 h-4 mr-1" />
                Logout
              </button>
            </div>
          ) : null}
        </div>

        <div className="md:hidden">
          <button onClick={toggleMenu}>
            {menuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {menuOpen && (
        <div className="md:hidden bg-white px-4 pt-2 pb-4 space-y-2 shadow">
          {!isAdmin && (
            <>
              <Link to="/home" className="block text-gray-700 hover:text-blue-600">
                Home
              </Link>
              <Link to="/contact" className="block text-gray-700 hover:text-blue-600">
                Contact
              </Link>
            </>
          )}
          {username && (
            <button
              onClick={handleLogout}
              className="w-full text-left text-gray-700 hover:text-blue-600"
            >
              Logout
            </button>
          )}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
