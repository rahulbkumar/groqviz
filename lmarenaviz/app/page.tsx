'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

const data = [
  { date: '2024-11-01', Google: 1303, OpenAI: 1340, Anthropic: 1286, DeepSeek: 1256, xAI: 1290, Mistral: 1251 },
  { date: '2024-12-01', Google: 1365, OpenAI: 1361, Anthropic: 1282, DeepSeek: 1258, xAI: 1289, Mistral: 1251 },
  { date: '2025-01-01', Google: 1373, OpenAI: 1365, Anthropic: 1283, DeepSeek: 1315, xAI: 1288, Mistral: 1251 },
  { date: '2025-02-01', Google: 1382, OpenAI: 1365, Anthropic: 1284, DeepSeek: 1358, xAI: 1288, Mistral: 1252 },
  { date: '2025-03-01', Google: 1385, OpenAI: 1377, Anthropic: 1313, DeepSeek: 1363, xAI: 1403, Mistral: 1251 },
  { date: '2025-04-01', Google: 1440, OpenAI: 1406, Anthropic: 1306, DeepSeek: 1370, xAI: 1404, Mistral: 1251 },
  { date: '2025-05-01', Google: 1439, OpenAI: 1418, Anthropic: 1301, DeepSeek: 1373, xAI: 1402, Mistral: 1251 },
  { date: '2025-06-01', Google: 1446, OpenAI: 1409, Anthropic: 1296, DeepSeek: 1368, xAI: 1399, Mistral: 1343 },
  { date: '2025-07-01', Google: 1473, OpenAI: 1428, Anthropic: 1372, DeepSeek: 1424, xAI: 1423, Mistral: 1369 },
  { date: '2025-08-01', Google: 1469, OpenAI: 1429, Anthropic: 1374, DeepSeek: 1425, xAI: 1435, Mistral: 1369 },
  { date: '2025-09-01', Google: 1470, OpenAI: 1429, Anthropic: 1373, DeepSeek: 1427, xAI: 1434, Mistral: 1370 },
]

const colors = {
  Google: '#fe9e20',
  OpenAI: '#f43e01',
  Anthropic: '#ffd1a3',
  DeepSeek: '#c23101',
  xAI: '#cecebf',
  Mistral: '#69695d',
}

export default function Home() {
  return (
    <div className="min-h-screen bg-background p-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-8">
          <h1 className="text-3xl font-light tracking-tight mb-2" style={{ letterSpacing: '0.85px' }}>
            LM Arena Leaderboard
          </h1>
          <p className="text-sm font-bold font-mono text-muted-foreground">
            AI Model Performance Scores Over Time
          </p>
        </div>

        <Card className="bg-card border-border">
          <CardHeader>
            <CardTitle className="text-sm font-bold" style={{ lineHeight: 1.2 }}>
              Model Score Trends
            </CardTitle>
            <CardDescription className="text-xs font-bold font-mono uppercase" style={{ lineHeight: 1.2 }}>
              Monthly performance metrics from November 2024 to September 2025
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="w-full h-96">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#2d2f33" />
                  <XAxis
                    dataKey="date"
                    stroke="#69695d"
                    style={{ fontSize: '12px' }}
                    tick={{ fill: '#cecebf' }}
                  />
                  <YAxis
                    domain={[1000, 1600]}
                    stroke="#69695d"
                    style={{ fontSize: '12px' }}
                    tick={{ fill: '#cecebf' }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#2d2f33',
                      border: '1px solid #69695d',
                      borderRadius: '8px',
                      boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.3)',
                    }}
                    labelStyle={{ color: '#ffffff' }}
                    itemStyle={{ color: '#ffffff' }}
                  />
                  <Legend
                    wrapperStyle={{
                      paddingTop: '20px',
                      color: '#cecebf',
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="Google"
                    stroke={colors.Google}
                    strokeWidth={2.5}
                    dot={false}
                    isAnimationActive={true}
                  />
                  <Line
                    type="monotone"
                    dataKey="OpenAI"
                    stroke={colors.OpenAI}
                    strokeWidth={2.5}
                    dot={false}
                    isAnimationActive={true}
                  />
                  <Line
                    type="monotone"
                    dataKey="Anthropic"
                    stroke={colors.Anthropic}
                    strokeWidth={2.5}
                    dot={false}
                    isAnimationActive={true}
                  />
                  <Line
                    type="monotone"
                    dataKey="DeepSeek"
                    stroke={colors.DeepSeek}
                    strokeWidth={2.5}
                    dot={false}
                    isAnimationActive={true}
                  />
                  <Line
                    type="monotone"
                    dataKey="xAI"
                    stroke={colors.xAI}
                    strokeWidth={2.5}
                    dot={false}
                    isAnimationActive={true}
                  />
                  <Line
                    type="monotone"
                    dataKey="Mistral"
                    stroke={colors.Mistral}
                    strokeWidth={2.5}
                    dot={false}
                    isAnimationActive={true}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <div className="mt-8 grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
          {Object.entries(colors).map(([provider, color]) => (
            <div key={provider} className="flex items-center gap-2 p-3 rounded-lg bg-card border border-border">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: color }}
              />
              <span className="text-sm font-medium text-foreground">{provider}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
