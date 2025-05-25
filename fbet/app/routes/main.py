from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.wallet import Wallet, Transaction
from app.forms.wallet_forms import DepositForm, WithdrawForm
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.wallet import Wallet, Transaction
from app.forms.wallet_forms import DepositForm, WithdrawForm
from app.models.sports import SportsGame, Bet
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError

from flask_wtf import FlaskForm
from wtforms import SelectField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

class BetForm(FlaskForm):
    game_id = SelectField('Game', coerce=int, validators=[DataRequired()])
    bet_type = SelectField('Bet Type', choices=[('home_win', 'Home Win'), ('away_win', 'Away Win'), ('draw', 'Draw')], validators=[DataRequired()])
    amount = DecimalField('Bet Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Place Bet')

@main_bp.route('/sports', methods=['GET', 'POST'])
@login_required
def sports():
    form = BetForm()
    games = SportsGame.query.order_by(SportsGame.start_time).all()
    form.game_id.choices = [(game.id, f"{game.team_home} vs {game.team_away} at {game.start_time.strftime('%Y-%m-%d %H:%M')}") for game in games]

    # Fetch user's bets with results
    user_bets = Bet.query.filter_by(user_id=current_user.id).all()

    if form.validate_on_submit():
        game = SportsGame.query.get(form.game_id.data)
        if not game:
            flash('Selected game not found.', 'danger')
            return redirect(url_for('main.sports'))

        amount = float(form.amount.data)
        wallet = Wallet.query.filter_by(user_id=current_user.id).first()
        if not wallet or wallet.balance < amount:
            flash('Insufficient balance to place bet.', 'danger')
            return redirect(url_for('main.sports'))

        # Deduct amount from wallet
        wallet.balance -= amount
        bet = Bet(user_id=current_user.id, game_id=game.id, bet_type=form.bet_type.data, amount=amount)
        db.session.add(bet)
        # Log transaction
        from app.models.wallet import Transaction
        txn = Transaction(wallet_id=wallet.id, amount=-amount, transaction_type='bet', description=f'Bet on game {game.id}')
        db.session.add(txn)
        db.session.commit()
        flash('Bet placed successfully.', 'success')
        return redirect(url_for('main.sports'))

    return render_template('sports.html', games=games, form=form, user_bets=user_bets)

from app.models.casino import CasinoGame

from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class CasinoBetForm(FlaskForm):
    amount = DecimalField('Bet Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Place Bet')

@main_bp.route('/casino', methods=['GET', 'POST'])
@login_required
def casino():
    form = CasinoBetForm()
    games = CasinoGame.query.all()

    # Fetch user's casino bets with results
    user_bets = Bet.query.filter_by(user_id=current_user.id).all()

    if form.validate_on_submit():
        game_id = int(request.form.get('game_id'))
        game = CasinoGame.query.get(game_id)
        if not game:
            flash('Selected game not found.', 'danger')
            return redirect(url_for('main.casino'))

        amount = float(form.amount.data)
        if amount < game.min_bet or amount > game.max_bet:
            flash(f'Bet amount must be between ${game.min_bet} and ${game.max_bet}.', 'danger')
            return redirect(url_for('main.casino'))

        wallet = Wallet.query.filter_by(user_id=current_user.id).first()
        if not wallet or wallet.balance < amount:
            flash('Insufficient balance to place bet.', 'danger')
            return redirect(url_for('main.casino'))

        # Deduct amount from wallet
        wallet.balance -= amount
        # Log transaction
        from app.models.wallet import Transaction
        txn = Transaction(wallet_id=wallet.id, amount=-amount, transaction_type='bet', description=f'Bet on casino game {game.id}')
        db.session.add(txn)
        db.session.commit()

        flash('Casino bet placed successfully.', 'success')
        return redirect(url_for('main.casino'))

    return render_template('casino.html', games=games, form=form, user_bets=user_bets)

@main_bp.route('/wallet', methods=['GET', 'POST'])
@login_required
def wallet():
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    if not wallet:
        wallet = Wallet(user_id=current_user.id, balance=0.0)
        db.session.add(wallet)
        db.session.commit()

    deposit_form = DepositForm(prefix='deposit')
    withdraw_form = WithdrawForm(prefix='withdraw')

    if deposit_form.validate_on_submit() and deposit_form.submit.data:
        amount = float(deposit_form.amount.data)
        wallet.balance += amount
        transaction = Transaction(wallet_id=wallet.id, amount=amount, transaction_type='deposit', description='Deposit')
        db.session.add(transaction)
        db.session.commit()
        flash(f'Deposited ${amount:.2f} successfully.', 'success')
        return redirect(url_for('main.wallet'))

    if withdraw_form.validate_on_submit() and withdraw_form.submit.data:
        amount = float(withdraw_form.amount.data)
        if amount > wallet.balance:
            flash('Insufficient balance for withdrawal.', 'danger')
        else:
            wallet.balance -= amount
            transaction = Transaction(wallet_id=wallet.id, amount=-amount, transaction_type='withdrawal', description='Withdrawal')
            db.session.add(transaction)
            db.session.commit()
            flash(f'Withdrew ${amount:.2f} successfully.', 'success')
        return redirect(url_for('main.wallet'))

    transactions = Transaction.query.filter_by(wallet_id=wallet.id).order_by(Transaction.timestamp.desc()).all()

    return render_template('wallet.html', wallet=wallet, deposit_form=deposit_form, withdraw_form=withdraw_form, transactions=transactions)
