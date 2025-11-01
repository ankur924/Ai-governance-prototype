import React, { useState } from "react";
import { AlertCircle, Eye, EyeOff, User, Lock, Mail } from "lucide-react";

function App() {
  const [currentPage, setCurrentPage] = useState("login");
  const [language, setLanguage] = useState("en");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  
  // Login/Register form states
  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [registerName, setRegisterName] = useState("");
  const [registerEmail, setRegisterEmail] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");
  const [registerConfirmPassword, setRegisterConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  
  // Complaint states
  const [complaint, setComplaint] = useState("");
  const [priority, setPriority] = useState(null);
  const [complaints, setComplaints] = useState([]);

  const translations = {
    en: {
      appName: "Nirakshak",
      tagline: "AI-Powered Governance System",
      login: "Login",
      register: "Register",
      logout: "Logout",
      email: "Email Address",
      password: "Password",
      confirmPassword: "Confirm Password",
      fullName: "Full Name",
      noAccount: "Don't have an account?",
      haveAccount: "Already have an account?",
      signUp: "Sign Up",
      signIn: "Sign In",
      welcome: "Welcome back",
      createAccount: "Create your account",
      title: "AI Governance Portal",
      subtitle: "Classify and Prioritize Citizen Grievances Automatically",
      complaint: "Enter your complaint",
      submit: "Submit Complaint",
      selectedLanguage: "Language",
      myComplaints: "My Complaints",
      priority: "Priority",
      status: "Status",
      pending: "Pending",
    },
    hi: {
      appName: "निरक्षक",
      tagline: "एआई-संचालित शासन प्रणाली",
      login: "लॉग इन करें",
      register: "रजिस्टर करें",
      logout: "लॉग आउट",
      email: "ईमेल पता",
      password: "पासवर्ड",
      confirmPassword: "पासवर्ड की पुष्टि करें",
      fullName: "पूरा नाम",
      noAccount: "खाता नहीं है?",
      haveAccount: "पहले से खाता है?",
      signUp: "साइन अप करें",
      signIn: "साइन इन करें",
      welcome: "वापसी पर स्वागत है",
      createAccount: "अपना खाता बनाएं",
      title: "एआई गवर्नेंस पोर्टल",
      subtitle: "शिकायतों को स्वचालित रूप से वर्गीकृत और प्राथमिकता दें",
      complaint: "अपनी शिकायत दर्ज करें",
      submit: "शिकायत सबमिट करें",
      selectedLanguage: "भाषा",
      myComplaints: "मेरी शिकायतें",
      priority: "प्राथमिकता",
      status: "स्थिति",
      pending: "लंबित",
    },
  };

  const t = translations[language];

  const handleLogin = () => {
    setError("");
    
    if (!loginEmail || !loginPassword) {
      setError("Please fill in all fields");
      return;
    }
    
    // Mock login - in production, this would call your backend
    setUser({ name: loginEmail.split("@")[0], email: loginEmail });
    setIsLoggedIn(true);
    setCurrentPage("dashboard");
    setLoginEmail("");
    setLoginPassword("");
  };

  const handleRegister = () => {
    setError("");
    
    if (!registerName || !registerEmail || !registerPassword || !registerConfirmPassword) {
      setError("Please fill in all fields");
      return;
    }
    
    if (registerPassword !== registerConfirmPassword) {
      setError("Passwords do not match");
      return;
    }
    
    if (registerPassword.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }
    
    // Mock registration - in production, this would call your backend
    setUser({ name: registerName, email: registerEmail });
    setIsLoggedIn(true);
    setCurrentPage("dashboard");
    setRegisterName("");
    setRegisterEmail("");
    setRegisterPassword("");
    setRegisterConfirmPassword("");
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
    setCurrentPage("login");
    setComplaints([]);
    setComplaint("");
    setPriority(null);
  };

  const handleComplaintSubmit = () => {
    if (!complaint.trim()) {
      return;
    }
    
    const priorities = ["Low", "Medium", "High", "Critical"];
    const randomPriority = priorities[Math.floor(Math.random() * priorities.length)];
    
    const newComplaint = {
      id: Date.now(),
      text: complaint,
      priority: randomPriority,
      status: "Pending",
      date: new Date().toLocaleDateString(),
    };
    
    setComplaints([newComplaint, ...complaints]);
    setPriority(randomPriority);
    setComplaint("");
    
    setTimeout(() => setPriority(null), 5000);
  };

  const getPriorityColor = (priority) => {
    const colors = {
      Low: "bg-blue-100 text-blue-700",
      Medium: "bg-yellow-100 text-yellow-700",
      High: "bg-orange-100 text-orange-700",
      Critical: "bg-red-100 text-red-700",
    };
    return colors[priority] || "bg-gray-100 text-gray-700";
  };

  const handleKeyPress = (e, action) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      action();
    }
  };

  // Login Page
  if (!isLoggedIn && currentPage === "login") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-2xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-indigo-600 mb-2">{t.appName}</h1>
            <p className="text-gray-500">{t.tagline}</p>
          </div>

          <div className="flex justify-end mb-4">
            <select
              className="border rounded-lg px-3 py-1 text-sm"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option value="en">English</option>
              <option value="hi">हिंदी</option>
            </select>
          </div>

          <h2 className="text-2xl font-semibold text-gray-800 mb-6">{t.welcome}</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700 text-sm">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {t.email}
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 text-gray-400" size={20} />
                <input
                  type="email"
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  value={loginEmail}
                  onChange={(e) => setLoginEmail(e.target.value)}
                  onKeyPress={(e) => handleKeyPress(e, handleLogin)}
                  placeholder="you@example.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {t.password}
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 text-gray-400" size={20} />
                <input
                  type={showPassword ? "text" : "password"}
                  className="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  onKeyPress={(e) => handleKeyPress(e, handleLogin)}
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            <button
              onClick={handleLogin}
              className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors"
            >
              {t.signIn}
            </button>
          </div>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              {t.noAccount}{" "}
              <button
                onClick={() => {
                  setCurrentPage("register");
                  setError("");
                }}
                className="text-indigo-600 font-semibold hover:underline"
              >
                {t.signUp}
              </button>
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Register Page
  if (!isLoggedIn && currentPage === "register") {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-2xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-indigo-600 mb-2">{t.appName}</h1>
            <p className="text-gray-500">{t.tagline}</p>
          </div>

          <div className="flex justify-end mb-4">
            <select
              className="border rounded-lg px-3 py-1 text-sm"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option value="en">English</option>
              <option value="hi">हिंदी</option>
            </select>
          </div>

          <h2 className="text-2xl font-semibold text-gray-800 mb-6">{t.createAccount}</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700 text-sm">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {t.fullName}
              </label>
              <div className="relative">
                <User className="absolute left-3 top-3 text-gray-400" size={20} />
                <input
                  type="text"
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  value={registerName}
                  onChange={(e) => setRegisterName(e.target.value)}
                  placeholder="John Doe"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {t.email}
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 text-gray-400" size={20} />
                <input
                  type="email"
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  value={registerEmail}
                  onChange={(e) => setRegisterEmail(e.target.value)}
                  placeholder="you@example.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {t.password}
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 text-gray-400" size={20} />
                <input
                  type={showPassword ? "text" : "password"}
                  className="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  value={registerPassword}
                  onChange={(e) => setRegisterPassword(e.target.value)}
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {t.confirmPassword}
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 text-gray-400" size={20} />
                <input
                  type={showPassword ? "text" : "password"}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  value={registerConfirmPassword}
                  onChange={(e) => setRegisterConfirmPassword(e.target.value)}
                  onKeyPress={(e) => handleKeyPress(e, handleRegister)}
                  placeholder="••••••••"
                />
              </div>
            </div>

            <button
              onClick={handleRegister}
              className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors"
            >
              {t.signUp}
            </button>
          </div>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              {t.haveAccount}{" "}
              <button
                onClick={() => {
                  setCurrentPage("login");
                  setError("");
                }}
                className="text-indigo-600 font-semibold hover:underline"
              >
                {t.signIn}
              </button>
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Dashboard Page
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-indigo-600">{t.appName}</h1>
            <p className="text-sm text-gray-500">{t.tagline}</p>
          </div>
          <div className="flex items-center gap-4">
            <select
              className="border rounded-lg px-3 py-1 text-sm"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
            >
              <option value="en">English</option>
              <option value="hi">हिंदी</option>
            </select>
            <div className="flex items-center gap-2 text-gray-700">
              <User size={20} />
              <span className="font-medium">{user?.name}</span>
            </div>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm"
            >
              {t.logout}
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">{t.title}</h2>
            <p className="text-gray-500 mb-6">{t.subtitle}</p>

            <div className="space-y-4">
              <textarea
                className="w-full border border-gray-300 p-3 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                rows="6"
                placeholder={t.complaint}
                value={complaint}
                onChange={(e) => setComplaint(e.target.value)}
              ></textarea>
              <button
                onClick={handleComplaintSubmit}
                className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition-colors"
              >
                {t.submit}
              </button>
            </div>

            {priority && (
              <div className="mt-4 p-4 bg-green-50 border border-green-200 text-green-700 rounded-lg text-center font-semibold">
                ✅ Complaint categorized as: <span className="uppercase">{priority}</span> {t.priority}
              </div>
            )}
          </div>

          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">{t.myComplaints}</h2>
            
            {complaints.length === 0 ? (
              <div className="text-center py-12 text-gray-400">
                <AlertCircle size={48} className="mx-auto mb-3 opacity-50" />
                <p>No complaints submitted yet</p>
              </div>
            ) : (
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {complaints.map((c) => (
                  <div key={c.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between mb-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getPriorityColor(c.priority)}`}>
                        {c.priority}
                      </span>
                      <span className="text-xs text-gray-500">{c.date}</span>
                    </div>
                    <p className="text-gray-700 text-sm mb-2">{c.text}</p>
                    <div className="flex items-center gap-2 text-xs text-gray-500">
                      <span className="font-medium">{t.status}:</span>
                      <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded">{t.pending}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;