import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

interface Message {
  role: 'student' | 'tutor';
  content: string;
}

interface TutorConfig {
  depth: string;
  learning_style: string;
  communication_style: string;
  tone_style: string;
  reasoning_framework: string;
  use_emojis: boolean;
  language: string;
}

const MathTutor: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentLevel, setCurrentLevel] = useState('Highschool');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const levels = ['Elementary', 'Highschool', 'College', 'Graduate'];

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const newMessage: Message = {
      role: 'student',
      content: inputMessage
    };

    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const config: TutorConfig = {
        depth: currentLevel,
        learning_style: "Active",
        communication_style: "Socratic",
        tone_style: "Encouraging",
        reasoning_framework: "Causal",
        use_emojis: true,
        language: "English"
      };

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tutor`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          config,
          chat_history: messages
            .map(m => `${m.role}: ${m.content}`)
            .join('\n')
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      setMessages(prev => [...prev, {
        role: 'tutor',
        content: data.response
      }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        role: 'tutor',
        content: "I apologize, but I encountered an error. Could you please try again?"
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col w-full max-w-4xl mx-auto h-[600px] bg-white rounded-lg shadow-lg">
      {/* Header with level selection */}
      <div className="p-4 border-b">
        <h1 className="text-2xl font-bold text-center mb-4">Pythagore Math Tutor</h1>
        <div className="flex justify-center gap-2">
          {levels.map((level) => (
            <button
              key={level}
              onClick={() => setCurrentLevel(level)}
              className={`px-4 py-2 rounded-lg transition-colors ${
                currentLevel === level
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 hover:bg-gray-200'
              }`}
            >
              {level}
            </button>
          ))}
        </div>
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.role === 'student' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`max-w-[80%] p-3 rounded-lg ${
                message.role === 'student'
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 p-3 rounded-lg">
              Thinking...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="p-4 border-t">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask your math question..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !inputMessage.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default MathTutor;