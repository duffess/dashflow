import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, TrendingUp } from 'lucide-react';

const InsightCard = () => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl p-6 text-white h-full"
    >
      <div className="flex items-center gap-2 mb-4">
        <Sparkles className="w-6 h-6" />
        <h3 className="text-lg font-semibold">Insight Automático</h3>
      </div>
      
      <div className="space-y-4">
        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 bg-green-400 rounded-full flex items-center justify-center flex-shrink-0">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="font-medium mb-1">CTR em alta!</p>
              <p className="text-sm text-blue-100">
                Sua campanha "Black Friday 2024" teve aumento de <strong>15.2%</strong> em CTR nos últimos 7 dias.
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
          <p className="text-sm text-blue-100">
            💡 <strong>Recomendação:</strong> Considere aumentar o orçamento desta campanha para maximizar os resultados positivos.
          </p>
        </div>
      </div>
    </motion.div>
  );
};

export default InsightCard;