import unittest
from ngram_model import Ngram_model
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Test_Ngram_model(unittest.TestCase):

  def setUp(self):
    self.text = """Eating is her subject.
       While eating is her subject.
       Where eating is her subject.
       Withdraw whether it is eating which is her subject. Literally
while she ate eating is her subject. Afterwards too and in be-
tween. This is an introduction to what she ate.
       She ate a pigeon and a soufflé.
       That was on one day.
       She ate a thin ham and its sauce.
       That was on another day.
       She ate desserts.
       That had been on one day.
       She had fish grouse and little cakes that was before that day.
       She had breaded veal and grapes that was on that day.
       After that she ate every day.
       Very little but very good.
       She ate very well that day.
       What is the difference between steaming and roasting, she
ate it cold because of Saturday.
       Remembering potatoes because of preparation for part of
the day.
       There is a difference in preparation of cray-fish which makes a
change in their fish for instance.
       What was it besides bread.
       Why is eating her subject.
       There are reasons why eating is her subject.
       Because.
       Help Helena.
       With whether a pound.
       Everybody who comes has been with whether we mean ours
allowed.
       Tea rose snuff box tea rose.
       Willed him well will till well.
       By higher but tire by cry my tie for her.
       Meeting with with said.
       Gain may be hours.
       There there their softness.
       By my buy high.
       By my softness.
       There with their willow with without out outmost lain in out.
       Has she had her tooth without a telegram.
       Nothing surprises Edith. Her sister made it once for all.
       Chair met alongside.
       Paved picnic with gratitude.
       He is strong and sturdy.
       Pile with a pretty boy.
       Having tired of some one.
       Tire try.
       Imagine how they felt when they were invited.
       Preamble to restitution.
       Tire and indifferent.
       Narratives with pistache.
       A partly boiled.
       Next sentence.
       Now or not nightly.
       A sentence it is a whether wither intended.
       A sentence text. Taxed.
       A sampler with ingredients may be unmixed with their ac-
counts how does it look like. If in way around. Like lightning.
       Apprehension is why they help to do what is in amount what
is an amount.
       A sentence felt way laid.
       A sentence without a horse.
       It is a mend that to distribute with send.
       A sentence is in a letter ladder latter.
       Birth with birth.
       If any thinks about what is made for the sake they will
manage to place taking take may.
       How are browns.
       How are browns.
       Got to go away.
       Anybody can be taught to love whatever whatever they like
better.
       Taught of butter.
       Whatever they like better.
       Unify is to repeat alike like letter.
       To a sentence.
       Answer do you need what it is vulnerable.
       There made an assay.
       Wire on duck.
       Please forget Kate.
       Please and do forbid how very well they like it.
       Paid it forbid forfeit a renewal.
       A sentence may be near by.
       Very well in eighty.
       If a letter with mine how are hear in all. This is to show that
a letter is better. Than seen.
       A sentence is money made beautiful. Beautiful words of
love. Really thought at a sentence very likely.
       How do you do they knew.
       A sentence made absurd.
       She is sure that he showed that he would be where a month.
       This is the leaf safe safety.
       This is the relief safe safely.
       A joined in compel commit comply angle of by and by with
all.
       Sorry to have been shaded easily by their hastened their
known go in find.
       In never indented never the less.
       As a wedding of their knowing with which whether they
could guess.
       Bewildered in infancy with compliments makes their agree-
ment strange.
       Houses have distributed in dividing with a pastime that they
called whose as it.
       Bent in view. With vein meant. Then at in impenetrable
covered with the same that it is having sent.
       Are eight seen to be pale apples.
       A sentence is a subterfuge refuge refuse for an admirable
record of their being in private admirable refuge for their being
in private this in vain their collide.
       A sentence controls does play shade.
       A sentence having been hours first.
       A sentence rest he likes a sentence lest best with interest.
       Induce sentences.
       A sentence makes them for stairs for stairs do bedew.
       A sentence about nothing in a sentence about nothing that
pale apples from rushing are best.
       No powder or power or power form form fortification in
vain of their verification of their very verification within with
whim with a whim which is in an implanted hour.
       Suppose a sentence.
       How are ours in glass.
       Glass makes ground glass.
       A sentence of their noun.
       How are you in invented complimented.
       How are you in in favourite.
       Thinking of sentences in complimented.
       Sentences in in complimented in thank in think in sentences
in think in complimented.
       Sentences should not shrink. Complimented.
       A sentence two sentences should not think complimented.
Complimented.
       How do you do if you are to to well complimented. A sen-
tence leans to along.
       Once when they went they made the name the same do do
climbed in a great many however they are that is why without
on account faired just as well as mention. Next they can come
being in tears, governess a part of plums comfort with our
aghast either by feel torn.
       How can whose but dear me oh.
       Darling how is George. George is well. Violate Thomas but
or must with pine and near and do and dare defy.
       Haynes is Mabel Haynes.
       What was what was what it was what is what is what is is
what is what which is what is is it.
       At since robbed of a pre prize sent.
       Tell a title.
       What was it that made him be mine what was it.
       Three years lack back back made well well willows three
years back.
       It never makes it bathe a face.
       How are how are how are how are how are heard. Weak-
ness is said.
       Jay James go in George Wilbur right with a prayed in de-
gree.
       We leave we form we regret.
       That these which with agrees adjoin comes clarity in eagle
quality that periodic when men calls radically readily read in
mean to mention.
       What is ate ate in absurd.
       Mathilda makes ours see.
       An epoch is identical with usury.
       A very long hour makes them hire lain down.
       Two tempting to them.
       Follow felt follow.
       He loves his aigrette too with mainly did in most she could
not newly instead dumb done entirely.
       Absurd our our absurd.
       With flight.
       Take him and think of him. He and think of him. With
him think of him. With him and with think with think with
think with him."""

  def test(self):
    model = Ngram_model(self.text, 3)
    self.assertTrue(len(model.model) == 3)


unittest.main()