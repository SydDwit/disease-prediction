import React, { useState } from "react";
import Navbar from "./Navbar";

const Contact = () => {
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState({ type: "", text: "" });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) {
      setStatus({ type: "error", text: "Please enter a message" });
      return;
    }

    setIsSubmitting(true);
    setStatus({ type: "", text: "" });

    try {
      const response = await fetch('http://localhost:8000/api/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) throw new Error('Failed to send message');

      setMessage("");
      setStatus({ type: "success", text: "Message sent successfully!" });
    } catch (err) {
      setStatus({ type: "error", text: "Failed to send message. Please try again." });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <div className="flex justify-center items-center h-[calc(100vh-4rem)] px-4">
        <div className="w-full max-w-md bg-white p-8 rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">Contact Us</h2>
          
          {status.text && (
            <div className={`mb-4 p-3 rounded ${
              status.type === "success" ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
            }`}>
              {status.text}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="message" className="block text-sm font-medium text-gray-700">Message</label>
              <textarea
                id="message"
                name="message"
                rows="6"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your message here..."
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              ></textarea>
            </div>
            
            <button
              type="submit"
              disabled={isSubmitting}
              className={`w-full px-4 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none transition-transform transform hover:scale-105 active:scale-95 
                ${isSubmitting ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {isSubmitting ? 'Sending...' : 'Send Message'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Contact;