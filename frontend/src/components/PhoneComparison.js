import React from 'react';
import { X, Smartphone, Camera, Battery, Cpu, HardDrive, DollarSign, Shield, Wifi } from 'lucide-react';

const PhoneComparison = ({ phones, onRemove, onClose }) => {
  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(price);
  };

  if (!phones || phones.length === 0) {
    return null;
  }

  const specs = [
    { key: 'price', label: 'Price', icon: DollarSign, format: formatPrice },
    { key: 'display_size', label: 'Display Size', icon: Smartphone, format: (val) => `${val}"` },
    { key: 'display_resolution', label: 'Resolution', icon: Smartphone, format: (val) => val || 'N/A' },
    { key: 'processor', label: 'Processor', icon: Cpu, format: (val) => val || 'N/A' },
    { key: 'ram', label: 'RAM', icon: Cpu, format: (val) => `${val}GB` },
    { key: 'storage', label: 'Storage', icon: HardDrive, format: (val) => `${val}GB` },
    { key: 'camera_main', label: 'Main Camera', icon: Camera, format: (val) => val || 'N/A' },
    { key: 'camera_front', label: 'Front Camera', icon: Camera, format: (val) => val || 'N/A' },
    { key: 'battery_capacity', label: 'Battery', icon: Battery, format: (val) => `${val}mAh` },
    { key: 'charging_speed', label: 'Charging', icon: Battery, format: (val) => val || 'N/A' },
    { key: 'weight', label: 'Weight', icon: Smartphone, format: (val) => `${val}g` },
    { key: 'water_resistance', label: 'Water Resistance', icon: Shield, format: (val) => val || 'N/A' },
    { key: 'wireless_charging', label: 'Wireless Charging', icon: Wifi, format: (val) => val ? 'Yes' : 'No' },
  ];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-xl font-bold text-gray-800">Phone Comparison</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <X className="w-6 h-6" />
          </button>
        </div>
        
        {/* Comparison Table */}
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-4 py-3 text-left text-sm font-medium text-gray-500">Specification</th>
                {phones.map((phone) => (
                  <th key={phone.id} className="px-4 py-3 text-center text-sm font-medium text-gray-500 min-w-[200px]">
                    <div className="flex flex-col items-center">
                      <div className="font-semibold text-gray-800 mb-1">{phone.name}</div>
                      <div className="text-xs text-gray-500">{phone.brand}</div>
                      <button
                        onClick={() => onRemove(phone.id)}
                        className="mt-2 text-red-500 hover:text-red-700 text-xs"
                      >
                        Remove
                      </button>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {specs.map((spec, index) => (
                <tr key={spec.key} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="px-4 py-3 text-sm font-medium text-gray-700 flex items-center">
                    <spec.icon className="w-4 h-4 mr-2" />
                    {spec.label}
                  </td>
                  {phones.map((phone) => (
                    <td key={phone.id} className="px-4 py-3 text-sm text-gray-600 text-center">
                      {spec.format(phone[spec.key])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {/* Footer */}
        <div className="p-4 border-t bg-gray-50">
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-500">
              Compare up to 3 phones at once
            </div>
            <button
              onClick={onClose}
              className="bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PhoneComparison;
