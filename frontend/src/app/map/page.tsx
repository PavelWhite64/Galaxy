'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

interface Plot {
  id: number;
  name: string | null;
  territory_id: number;
  owner_id: number;
  plot_type: string;
  area: number;
  coordinates: any;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export default function MapPage() {
  const [plots, setPlots] = useState<Plot[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPlot, setSelectedPlot] = useState<Plot | null>(null);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/login');
      return;
    }

    fetchPlots();
  }, [router]);

  const fetchPlots = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/plots/`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        }
      );
      setPlots(response.data);
    } catch (error) {
      console.error('Failed to fetch plots:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClaimPlot = async (plotId: number) => {
    try {
      await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/plots/${plotId}/claim`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        }
      );
      fetchPlots();
      alert('Plot claimed successfully!');
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to claim plot');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-gray-400">Loading world map...</div>
      </div>
    );
  }

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <header className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
            World Map
          </h1>
          <button
            onClick={() => {
              localStorage.removeItem('access_token');
              router.push('/');
            }}
            className="px-4 py-2 border border-red-600 text-red-500 hover:border-red-400 rounded-lg transition"
          >
            Logout
          </button>
        </header>

        <div className="grid md:grid-cols-3 gap-6">
          {/* Plot Grid */}
          <div className="md:col-span-2">
            <div className="bg-gray-900 rounded-xl border border-gray-800 p-6">
              <h2 className="text-xl font-semibold mb-4">Available Plots</h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                {plots.map((plot) => (
                  <div
                    key={plot.id}
                    onClick={() => setSelectedPlot(plot)}
                    className={`p-4 rounded-lg border cursor-pointer transition ${
                      plot.is_active
                        ? 'bg-green-900/30 border-green-700 hover:border-green-500'
                        : 'bg-gray-800 border-gray-700 hover:border-blue-500'
                    }`}
                  >
                    <div className="text-sm font-medium truncate">{plot.name || `Plot #${plot.id}`}</div>
                    <div className="text-xs text-gray-400 mt-1">{plot.plot_type}</div>
                    <div className="text-xs text-gray-500 mt-1">{plot.area} units²</div>
                    <div className={`text-xs mt-2 ${plot.is_active ? 'text-green-400' : 'text-gray-500'}`}>
                      {plot.is_active ? 'Owned' : 'Available'}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Plot Details Panel */}
          <div>
            <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 sticky top-8">
              <h2 className="text-xl font-semibold mb-4">Plot Details</h2>
              {selectedPlot ? (
                <div className="space-y-4">
                  <div>
                    <div className="text-sm text-gray-400">Name</div>
                    <div className="font-medium">{selectedPlot.name || `Plot #${selectedPlot.id}`}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-400">Type</div>
                    <div className="font-medium capitalize">{selectedPlot.plot_type}</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-400">Area</div>
                    <div className="font-medium">{selectedPlot.area} units²</div>
                  </div>
                  <div>
                    <div className="text-sm text-gray-400">Status</div>
                    <div className={`font-medium ${selectedPlot.is_active ? 'text-green-400' : 'text-blue-400'}`}>
                      {selectedPlot.is_active ? 'Owned' : 'Available'}
                    </div>
                  </div>
                  {!selectedPlot.is_active && (
                    <button
                      onClick={() => handleClaimPlot(selectedPlot.id)}
                      className="w-full py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition"
                    >
                      Claim This Plot
                    </button>
                  )}
                </div>
              ) : (
                <div className="text-gray-400 text-sm">
                  Select a plot to view details
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
