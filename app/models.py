# Imports
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import *
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist

# Decks class
class Deck(models.Model):
    id = models.AutoField(primary_key=True)

    user_account =  models.ForeignKey(User, on_delete=models.DO_NOTHING)
    creator_username = models.CharField(blank=False, max_length=50)
    deckName = models.CharField(blank=False, max_length=50)
    dateCreated = models.DateField(null=True, blank=True)
    isFavourite = models.BooleanField(default=False)
    editable = models.BooleanField(default=False)
    cardCount = models.IntegerField(default=0)

    # Decks Methods below

    def __str__(self):
        return self.deckName

    # returns QuerySet for all decks of User
    def getUsersDecks(user_ID):
        decks = Deck.objects.filter(user_account__id = user_ID)
        return decks

    # returns single deck object
    def getDeck(deck_ID, user_ID):
        try:
            deck = Deck.objects.get(id = deck_ID, user_account__id = user_ID)
        except ObjectDoesNotExist:
            deck = False
        return deck
    def createDeck(deck_name, user_acc):
        new_deck = Deck(user_account = user_acc, creator_username = user_acc.username, deckName = deck_name, dateCreated = datetime.today(), editable = True )
        new_deck.save()
        return
    
    def deleteDeck(deckId):
        cards = Card.objects.filter(deck__id = deckId)
        for card in cards:
            try:
                Card.deleteCard(deckId, card.id)
            except:
                pass
        Deck.objects.filter(id = deckId).delete()
        return

    def shareDeck(deckId, username):
        user_acc = User.objects.get(username = username)
        deck = Deck.objects.get(id = deckId)
        new_deck = Deck(id = deckId, user_account = user_acc, creator_username = deck.creator_username, deckName = deck.deckName)
        new_deck.save()
        #cards = Card.getDecksCards(deckId)

        # for card in cards:
        #     CardLedger.createLedger(new_deck, user_acc, card)

        return


# Cards class
class Card(models.Model):
    id = models.AutoField(primary_key=True)

    deck = models.ForeignKey(Deck, on_delete = models.DO_NOTHING)
    
    front_text = models.CharField(max_length=280)
    back_text = models.CharField(max_length=280)
    front_Img = models.ImageField(upload_to='images/', null=True, blank=True)
    back_Img = models.ImageField(upload_to='images/', null=True, blank=True)

    # Cards Methods below

    def __str__(self):
        return self.front_text

    # returns all of the cards in a specific users deck
    def getDecksCards(deck_ID):
        try:
            cards = Card.objects.filter(deck__id = deck_ID)
        except ObjectDoesNotExist:
            cards = False
        return cards
    
    def getStudyCard(studyLedger):
        studyCard = Card.objects.get(id = studyLedger.card.id)
        studyTuple = [studyCard, studyLedger.id]

        return studyTuple
    
    #NEED TO UPDATE TO CREATE LEDGER FOR EVERY USER WHO HAS DECK
    def createCard(deck_obj, cardInfo, user_acc):
        newCard = Card(deck=deck_obj, front_text = cardInfo['frontText'], back_text = cardInfo['backText'], front_Img = cardInfo['frontImg'], back_Img = cardInfo['backImg'])
        newCard.save()

        CardLedger.createLedger(deck_obj, user_acc, newCard)

        return
    
    def deleteCard(deckId, cardId):
        CardLedger.deleteLedger(deckId, cardId)
        card = Card.objects.filter(id = cardId, deck__id = deckId)
        for img in card:
            try:
                img.front_Img.delete()
            except:
                pass
            try:
                img.back_Img.delete()
            except:
                pass
            img.delete()
        return

class CardLedger(models.Model):
    id = models.AutoField(primary_key=True)

    deck = models.ForeignKey(Deck, on_delete = models.DO_NOTHING)
    user_account = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    card = models.ForeignKey(Card, on_delete=models.DO_NOTHING)

    study_date = models.DateField(default = None)
    ELO = models.IntegerField(default= 0 )
    leech = models.IntegerField(default=0)

    def __str__(self):
        return "User ID: {}, Deck ID: {}, Card ID: {}".format(self.user_account.id, self.deck.id, self.card.id)
    
    def getNumberofDueCards(deck_ID, user_ID):
        dueCards = CardLedger.objects.filter(deck__id = deck_ID, user_account__id = user_ID, study_date__lte = datetime.today()).count()
        return dueCards

    def getDueCards(deck_ID, user_ID):
        dueCards = CardLedger.objects.filter(deck__id = deck_ID, user_account__id = user_ID, study_date__lte = datetime.today())
        return dueCards

    def getDueCard(deck_ID, user_ID):
        dueCards = CardLedger.objects.filter(deck__id = deck_ID, user_account__id = user_ID, study_date__lte = datetime.today())[:1]
        
        if not dueCards:
            dueCards = False

        return dueCards
    
    def createLedger(deck_obj, user_acc, card_obj):
        newLedger = CardLedger(deck = deck_obj, user_account = user_acc, card = card_obj, study_date = datetime.today())
        newLedger.save()
        
        return
    
    def deleteLedger(deckId, cardId):
        CardLedger.objects.filter(deck__id = deckId, card__id = cardId).delete()
        return

    def updateLedger(cardLedgerId, seconds, choice):
        ledger = CardLedger.objects.get(id = cardLedgerId)
        if choice == 1:
            ledger.ELO = 0
            ledger.save()
            return

        newELO = ledger.ELO / 2
        if ledger.ELO == 0:
            newELO = 300
            ledger.ELO = newELO
            numberOfDays = ledger.ELO % 100
            ledger.study_date = datetime.today() + timedelta(days = numberOfDays)
            ledger.save()
            return

        if choice == 2:
            ledger.ELO += newELO
            numberOfDays = ledger.ELO % 100
            ledger.study_date = datetime.today() + timedelta(days = numberOfDays)
            ledger.save()
        elif choice == 3:
            ledger.ELO += newELO * 1.5
            numberOfDays = ledger.ELO % 100
            ledger.study_date = datetime.today() + timedelta(days = numberOfDays)
            ledger.save()
        

        return