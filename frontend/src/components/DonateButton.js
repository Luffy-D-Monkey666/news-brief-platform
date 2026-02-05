import React, { useState } from 'react';
import { FaHeart } from 'react-icons/fa';

const DonateButton = () => {
  const [showQRCodes, setShowQRCodes] = useState(false);
  const [modalImage, setModalImage] = useState(null);

  const toggleQRCodes = () => {
    setShowQRCodes(!showQRCodes);
  };

  const openModal = (imageSrc) => {
    setModalImage(imageSrc);
  };

  const closeModal = () => {
    setModalImage(null);
  };

  return (
    <div className="relative">
      {/* 打赏按钮 */}
      <button
        onClick={toggleQRCodes}
        className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-all duration-200 shadow-md hover:shadow-lg"
      >
        <FaHeart className="text-lg" />
        <span className="font-medium">打赏开发者</span>
      </button>

      {/* 二维码展示区域 */}
      {showQRCodes && (
        <div className="absolute top-full right-0 mt-2 bg-white rounded-lg shadow-2xl p-4 min-w-[300px] z-50 border border-gray-200">
          <div className="text-center mb-3">
            <p className="text-gray-700 font-medium">感谢您的支持</p>
            <p className="text-gray-500 text-sm mt-1">请扫描二维码打赏</p>
          </div>

          <div className="flex flex-col gap-4">
            {/* 微信支付二维码 */}
            <div className="text-center">
              <p className="text-sm text-gray-600 mb-2">微信支付</p>
              <img
                src="/donate/wechat-pay.jpg"
                alt="微信支付"
                className="w-full cursor-pointer hover:opacity-90 transition-opacity rounded-md"
                onClick={() => openModal('/donate/wechat-pay.jpg')}
              />
            </div>

            {/* 支付宝二维码 */}
            <div className="text-center">
              <p className="text-sm text-gray-600 mb-2">支付宝</p>
              <img
                src="/donate/alipay.jpg"
                alt="支付宝"
                className="w-full cursor-pointer hover:opacity-90 transition-opacity rounded-md"
                onClick={() => openModal('/donate/alipay.jpg')}
              />
            </div>
          </div>
        </div>
      )}

      {/* 大图模态框 */}
      {modalImage && (
        <div
          className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-[100] p-4"
          onClick={closeModal}
        >
          <div className="relative max-w-2xl max-h-[90vh]">
            <img
              src={modalImage}
              alt="二维码大图"
              className="max-w-full max-h-[90vh] object-contain"
              onClick={(e) => e.stopPropagation()}
            />
            <button
              onClick={closeModal}
              className="absolute top-4 right-4 bg-white text-black rounded-full w-10 h-10 flex items-center justify-center hover:bg-gray-200 transition-colors"
            >
              ✕
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DonateButton;
