import { NextRequest, NextResponse } from 'next/server'
import OpenAI from 'openai'

const SYSTEM_PROMPT = `You are an expert fashion tech pack writer and tailoring business consultant.
Output structured, professional garment specifications.
Always output valid JSON when the user requests a tech pack.
Be precise about measurements. All measurements in centimetres.`

export async function POST(req: NextRequest) {
  const { description, image_analysis } = await req.json()

  const apiKey = process.env.OPENAI_API_KEY
  if (!apiKey) {
    return NextResponse.json(stubCopilotResponse(description))
  }

  const client = new OpenAI({ apiKey })
  const prompt = buildPrompt(description, image_analysis)

  const t0 = Date.now()
  const completion = await client.chat.completions.create({
    model: process.env.MODEL_NAME ?? 'gpt-4o',
    messages: [
      { role: 'system', content: SYSTEM_PROMPT },
      { role: 'user', content: prompt },
    ],
    max_tokens: 1500,
    temperature: 0.3,
  })

  const text = completion.choices[0].message.content ?? ''
  const tech_pack = parseTechPack(text)
  const fabric_estimate = estimateFabric(tech_pack.fabric_type, tech_pack.fabric_yards)
  const price_quote = calculatePrice(fabric_estimate.fabric_cost_ngn, tech_pack.complexity, tech_pack.estimated_hours)

  return NextResponse.json({
    tech_pack,
    price_quote,
    fabric_estimate,
    summary_md: formatSummary(tech_pack, price_quote, fabric_estimate),
    latency_ms: Date.now() - t0,
  })
}

function buildPrompt(description: string, image_analysis?: string): string {
  let ctx = description
  if (image_analysis) ctx += `\n\nImage analysis:\n${image_analysis}`

  return `Create a complete tech pack for:\n\n${ctx}\n\n` +
    `Output a JSON object with: garment_name, description, category, silhouette, ` +
    `fabric_type (ankara/lace/cotton/etc), fabric_yards (float), colour, lining, closure, ` +
    `sleeves, collar, pockets, complexity (simple/moderate/complex/couture), ` +
    `estimated_hours (float), special_notes (array), construction_order (array).`
}

function parseTechPack(text: string): Record<string, unknown> & {
  fabric_type: string; fabric_yards: number; complexity: string; estimated_hours: number
} {
  try {
    const start = text.indexOf('{')
    const end = text.lastIndexOf('}') + 1
    return JSON.parse(text.slice(start, end))
  } catch {
    return {
      garment_name: 'Garment', description: text,
      fabric_type: 'ankara', fabric_yards: 4.0,
      complexity: 'moderate', estimated_hours: 6.0,
      special_notes: [], construction_order: [],
    }
  }
}

const FABRIC_PRICES: Record<string, number> = {
  ankara: 1800, lace: 4500, kente: 8000, 'aso-oke': 6500,
  chiffon: 2200, cotton: 1500, silk: 5500, velvet: 3800, denim: 2000,
}

function estimateFabric(fabric_type: string, yards: number) {
  const price = FABRIC_PRICES[fabric_type?.toLowerCase()] ?? 2000
  const cost = price * yards
  return {
    fabric_type, yards,
    price_per_yard_ngn: price,
    fabric_cost_ngn: Math.round(cost),
    cost_with_markup_ngn: Math.round(cost * 1.2),
    note: 'Add 10% for print matching on patterned fabrics',
  }
}

const COMPLEXITY: Record<string, number> = { simple: 1.0, moderate: 1.5, complex: 2.5, couture: 4.0 }

function calculatePrice(fabric_cost_ngn: number, complexity: string, hours: number) {
  const labour = 1500 * hours * (COMPLEXITY[complexity] ?? 1.5)
  const overhead = (fabric_cost_ngn + labour) * 0.15
  const subtotal = fabric_cost_ngn + labour + overhead
  const profit = subtotal * 0.25
  const total = subtotal + profit
  return {
    complexity, labour_hours: hours,
    fabric_cost_ngn: Math.round(fabric_cost_ngn),
    labour_cost_ngn: Math.round(labour),
    overhead_ngn: Math.round(overhead),
    profit_ngn: Math.round(profit),
    total_ngn: Math.round(total),
    total_usd_approx: Math.round(total / 1600 * 100) / 100,
    breakdown_pct: {
      fabric: Math.round(fabric_cost_ngn / total * 100 * 10) / 10,
      labour: Math.round(labour / total * 100 * 10) / 10,
      overhead: Math.round(overhead / total * 100 * 10) / 10,
      profit: Math.round(profit / total * 100 * 10) / 10,
    },
  }
}

function formatSummary(tech_pack: Record<string, unknown>, price: ReturnType<typeof calculatePrice>, fabric: ReturnType<typeof estimateFabric>): string {
  const name = tech_pack.garment_name as string ?? 'Garment'
  const notes = (tech_pack.special_notes as string[] ?? []).map(n => `- ${n}`).join('\n')
  const steps = (tech_pack.construction_order as string[] ?? []).join('\n')
  return `# Tech Pack: ${name}\n\n## Price Quote\n| Item | ₦ |\n|---|---|\n| Fabric | ${price.fabric_cost_ngn.toLocaleString()} |\n| Labour | ${price.labour_cost_ngn.toLocaleString()} |\n| Overhead | ${price.overhead_ngn.toLocaleString()} |\n| **Total** | **${price.total_ngn.toLocaleString()}** |\n\n> ~$${price.total_usd_approx} USD\n\n## Special Notes\n${notes || 'None'}\n\n## Construction Order\n${steps || 'See tech pack'}\n`
}

function stubCopilotResponse(description: string) {
  const fabric_estimate = estimateFabric('ankara', 4.5)
  const price_quote = calculatePrice(fabric_estimate.fabric_cost_ngn, 'complex', 12)
  const tech_pack = {
    garment_name: 'Corporate Ankara Blazer',
    description,
    category: 'Outerwear',
    silhouette: 'Fitted / Structured',
    fabric_type: 'ankara',
    fabric_yards: 4.5,
    colour: 'Navy + Gold Print',
    lining: 'Polyester lining, full body',
    closure: '3 × functional buttons, front',
    sleeves: '3/4 length, 2-button cuff',
    collar: 'Notch lapel',
    complexity: 'complex',
    estimated_hours: 12,
    special_notes: [
      'Match print at centre front and shoulder seams',
      'Pad stitch lapels by hand for structure',
      'Press all seams flat with tailor\'s ham',
    ],
    construction_order: [
      '1. Interface all structural pieces',
      '2. Sew and press all darts',
      '3. Construct welt pockets',
      '4. Join shoulder seams',
      '5. Set sleeves',
      '6. Attach collar and lapels',
      '7. Join side seams',
      '8. Attach lining',
      '9. Sew buttons and buttonholes',
      '10. Final pressing',
    ],
  }
  return {
    tech_pack,
    price_quote,
    fabric_estimate,
    summary_md: formatSummary(tech_pack, price_quote, fabric_estimate),
    latency_ms: 0,
  }
}
