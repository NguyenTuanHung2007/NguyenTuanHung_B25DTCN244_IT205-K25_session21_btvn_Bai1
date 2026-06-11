import logging
import os

logging.basicConfig(
    filename='momo_transactions.log',
    level=logging.INFO,
    format=['%(asctime)s - %(levelname)s - %(message)s'],
    encoding='utf-8'
)

balance = 0

class InvalidAmountError(Exception): pass
class InsufficientBalanceError(Exception): pass

def deposit_logic(amount):
    global balance
    if amount <= 0:
        logging.error(f'InvalidAmountError: Attempted to process {amount} VND.')
        raise InvalidAmountError(f'Attempted to process {amount} VND.')
    
    balance += amount
    logging.info(f'Deposit successful: +{amount} VND. Current Balance: {balance}')
    return balance

def transfer_logic(amount, phone):
    global balance
    if amount <= 0:
        logging.error(f'InvalidAmountError: Attempted to process {amount} VND.')
        raise InvalidAmountError(f'Attempted to process {amount} VND.')
    
    if amount > balance:
        logging.error(f'InsufficientBalanceError: Attempted to transfer {amount} VND with balance {balance} VND.')
        raise InsufficientBalanceError(f'Attempted to transfer {amount} VND with balance {balance} VND.')
    
    if amount >= 10000000:
        logging.warning(f'High value transaction detected: {amount} VND to {phone}')

    balance -= amount
    logging.info(f'Transfer successful: -{amount} VND to {phone}. Current Balance: {balance}')
    return balance

def handle_deposit():
    print('\n--- NẠP TIỀN VÀO VÍ ---')
    try:
        val = input('Nhập số tiền cần nạp: ')
        amount = int(val)
        new_balance = deposit_logic(amount)
        print(f'\nNạp tiền thành công: +{amount:,} VND')
        print(f'Số dư hiện tại: {new_balance:,} VND')
    except ValueError:
        logging.error('ValueError: Invalid numeric input for deposit.')
        print('\nLỗi: Vui lòng nhập số tiền hợp lệ.')
    except InvalidAmountError:
        print('\nLỗi: Số tiền giao dịch phải lớn hơn 0.')

def handle_transfer():
    print('\n--- CHUYỂN TIỀN ---')
    phone = input('Nhập số điện thoại người nhận: ').strip()
    if len(phone) != 10 or not phone.isdigit():
        print('Lỗi: Số điện thoại phải đúng định dạng 10 số.')
        return
    
    try:
        val = input('Nhập số tiền cần chuyển: ')
        amount = int(val)
        new_balance = transfer_logic(amount, phone)
        print(f'\nChuyển tiền thành công tới số điện thoại {phone}.')
        print(f'Số tiền đã chuyển: {amount:,} VND')
        print(f'Số dư còn lại: {new_balance:,} VND')
    except ValueError:
        logging.error('ValueError: Invalid numeric input for transfer.')
        print('\nLỗi: Vui lòng nhập số tiền hợp lệ.')
    except InvalidAmountError:
        print('\nLỗi: Số tiền giao dịch phải lớn hơn 0.')
    except InsufficientBalanceError:
        print('\nGiao dịch thất bại: Số dư của bạn không đủ.')

def read_system_logs():
    if not os.path.exists('momo_transactions.log'):
        print('Chưa có lịch sử giao dịch nào trong hệ thống.')
        return

    print('\n--- 5 SỰ KIỆN GẦN NHẤT TRONG HỆ THỐNG ---')
    with open('momo_transactions.log', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[-5:], 1):
            print(f'{i}. {line.strip()}')

def show_balance():
    logging.info(f'Balance checked. Current Balance: {balance}')
    print('\n--- SỐ DƯ VÍ MOMO ---')
    print(f'Số dư hiện tại: {balance:,} VND')

def main():
    while True:
        print('\n========== VÍ MOMO GIẢ LẬP ==========')
        print('1. Nạp tiền vào ví')
        print('2. Chuyển tiền')
        print('3. Xem lịch sử hệ thống')
        print('4. Xem số dư tài khoản')
        print('5. Thoát chương trình')
        print('=====================================')
        
        choice = input('Chọn chức năng (1-5): ')
        
        if choice == '1':
            handle_deposit()
        elif choice == '2':
            handle_transfer()
        elif choice == '3':
            read_system_logs()
        elif choice == '4':
            show_balance()
        elif choice == '5':
            print('Cảm ơn bạn đã sử dụng dịch vụ')
            logging.info('System shutdown')
            break
        else:
            print('Lựa chọn không hợp lệ.')

if __name__ == '__main__':
    main()