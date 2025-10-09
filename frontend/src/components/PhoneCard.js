import React from 'react';
import { Smartphone, Camera, Battery, Cpu, HardDrive, DollarSign } from 'lucide-react';

const PhoneCard = ({ phone, onCompare, isSelected = false }) => {
  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(price);
  };

  const handleCompareClick = () => {
    onCompare(phone.id);
  };

  return (
    <div className={`bg-white rounded-lg shadow-md border-2 transition-all duration-200 hover:shadow-lg ${
      isSelected ? 'border-primary-500' : 'border-gray-200'
    }`}>
      {/* Phone Image */}
      <div className="h-48 bg-gray-100 rounded-t-lg flex items-center justify-center">
        {phone.image_url ? (
          <img 
            src={phone.image_url} 
            alt={phone.name}
            className="h-full w-full object-contain rounded-t-lg"
            onError={(e) => {
              e.target.style.display = 'none';
              e.target.nextSibling.style.display = 'flex';
            }}
          />
        ) : null}
        <div className="flex items-center justify-center h-full w-full" style={{ display: phone.image_url ? 'none' : 'flex' }}>
          <Smartphone className="w-16 h-16 text-gray-400" />
        </div>
      </div>
      
      {/* Phone Details */}
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="font-semibold text-lg text-gray-800 line-clamp-2">{phone.name}</h3>
          <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">{phone.brand}</span>
        </div>
        
        <div className="flex items-center mb-3">
          <DollarSign className="w-4 h-4 text-green-600 mr-1" />
          <span className="text-xl font-bold text-green-600">{formatPrice(phone.price)}</span>
        </div>
        
        {/* Key Specs */}
        <div className="space-y-2 mb-4">
          {phone.camera_main && (
            <div className="flex items-center text-sm text-gray-600">
              <Camera className="w-4 h-4 mr-2" />
              <span>{phone.camera_main}</span>
            </div>
          )}
          
          {phone.ram && (
            <div className="flex items-center text-sm text-gray-600">
              <Cpu className="w-4 h-4 mr-2" />
              <span>{phone.ram}GB RAM</span>
            </div>
          )}
          
          {phone.storage && (
            <div className="flex items-center text-sm text-gray-600">
              <HardDrive className="w-4 h-4 mr-2" />
              <span>{phone.storage}GB Storage</span>
            </div>
          )}
          
          {phone.battery_capacity && (
            <div className="flex items-center text-sm text-gray-600">
              <Battery className="w-4 h-4 mr-2" />
              <span>{phone.battery_capacity}mAh</span>
            </div>
          )}
        </div>
        
        {/* Features */}
        {phone.features && (
          <div className="mb-4">
            <p className="text-xs text-gray-500 line-clamp-2">{phone.features}</p>
          </div>
        )}
        
        {/* Action Button */}
        <button
          onClick={handleCompareClick}
          className={`w-full py-2 px-4 rounded-lg font-medium transition-colors ${
            isSelected
              ? 'bg-primary-600 text-white'
              : 'bg-primary-500 text-white hover:bg-primary-600'
          }`}
        >
          {isSelected ? 'Selected for Comparison' : 'Add to Comparison'}
        </button>
      </div>
    </div>
  );
};

export default PhoneCard;
