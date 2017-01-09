package simplifier

import AST._

// to implement
// avoid one huge match of cases
// take into account non-greedy strategies to resolve cases with power laws
object Simplifier {

  def simplify(node: Node): Node = {
    node match {
      case Unary(op, expr) => simplifyUnary(op, simplify(expr))
      case BinExpr(op, left, right) => simplifyBinExpr(op, simplify(left), simplify(right))
      case IfElseExpr(cond, left, right) =>
        simplify(cond) match {
          case TrueConst() => simplify(left)
          case FalseConst() => simplify(right)
        }
      case Assignment(left, right) if left == right => NodeList(nil)
      case Assignment(left, right) => Assignment(left, simplify(right))
      case Subscription(expr, sub) => Subscription(simplify(expr), simplify(sub))
      case KeyDatum(key, value) => KeyDatum(key, simplify(value))
      case IfInstr(cond, left) =>
        simplify(cond) match {
          case TrueConst() => simplify(left)
        }
      case IfElseInstr(cond, left, right) =>
        simplify(cond) match {
          case TrueConst() => simplify(left)
          case FalseConst() => simplify(right)
        }
      case WhileInstr(cond, body) =>
        simplify(cond) match {
          case TrueConst() => simplify(body)
        }
      case ReturnInstr(expr) => ReturnInstr(simplify(expr))
      case PrintInstr(expr) => PrintInstr(simplify(expr))
      case FunDef(name, formal_args, body) => FunDef(name, formal_args, simplify(body))
      case LambdaDef(formal_args, body) => LambdaDef(formal_args, simplify(body))
      case NodeList(list) => simplifyNodeList(list)
      case KeyDatumList(list) => simplifyDatumList(list)
      case IdList(list) =>
      case ElemList(list) =>
      case Tuple(list) =>
      case node => node
    }
  }

  def simplifyUnary(_op: String, _expr: Node): Node = {
    val neg_op = Map(
      "==" -> "!=",
      "!=" -> "==",
      "<" -> ">=",
      ">" -> "<=",
      "<=" -> ">",
      ">=" -> "<"
    )

    (_op, _expr) match {
      case ("not", BinExpr(op, left, right)) if neg_op.contains(op) =>
        BinExpr(neg_op(op), left, right)
      case ("not", Unary("not", expr)) => expr
      case ("not", TrueConst()) => FalseConst()
      case ("not", FalseConst()) => TrueConst()
      case ("-", Unary("-", expr)) => expr
      case (op, expr) => Unary(op, expr)
    }
  }

  def simplifyBinExpr(_op: String, _left : Node, _right : Node): Node = {

  }

  def simplifyNodeList(_list: List[Node]): Node = {
  }

  def simplifyDatumList(_list: List[Node]): Node = {

  }

  def isZero(node: Node): Boolean = {
    node match {
      case IntNum(0) => true
      case FloatNum(0.0) => true
      case _ => false
    }
  }

  def isOne(node: Node): Boolean = {
    node match {
      case IntNum(1) => true
      case FloatNum(1.0) => true
      case _ => false
    }
  }

}
